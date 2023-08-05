use rustpython_parser::ast::{Arguments, Constant, Expr, ExprKind};

use ruff_diagnostics::Violation;
use ruff_diagnostics::{Diagnostic, DiagnosticKind};
use ruff_macros::{derive_message_formats, violation};
use ruff_python_ast::call_path::from_qualified_name;
use ruff_python_ast::call_path::{compose_call_path, CallPath};
use ruff_python_ast::types::Range;
use ruff_python_ast::visitor;
use ruff_python_ast::visitor::Visitor;

use crate::checkers::ast::Checker;

use super::mutable_argument_default::is_mutable_func;

#[violation]
pub struct FunctionCallInDefaultArgument {
    pub name: Option<String>,
}

impl Violation for FunctionCallInDefaultArgument {
    #[derive_message_formats]
    fn message(&self) -> String {
        let FunctionCallInDefaultArgument { name } = self;
        if let Some(name) = name {
            format!("Do not perform function call `{name}` in argument defaults")
        } else {
            format!("Do not perform function call in argument defaults")
        }
    }
}

const IMMUTABLE_FUNCS: &[&[&str]] = &[
    &["", "tuple"],
    &["", "frozenset"],
    &["datetime", "date"],
    &["datetime", "datetime"],
    &["datetime", "timedelta"],
    &["decimal", "Decimal"],
    &["operator", "attrgetter"],
    &["operator", "itemgetter"],
    &["operator", "methodcaller"],
    &["pathlib", "Path"],
    &["types", "MappingProxyType"],
    &["re", "compile"],
];

fn is_immutable_func(checker: &Checker, func: &Expr, extend_immutable_calls: &[CallPath]) -> bool {
    checker
        .ctx
        .resolve_call_path(func)
        .map_or(false, |call_path| {
            IMMUTABLE_FUNCS
                .iter()
                .any(|target| call_path.as_slice() == *target)
                || extend_immutable_calls
                    .iter()
                    .any(|target| call_path == *target)
        })
}

struct ArgumentDefaultVisitor<'a> {
    checker: &'a Checker<'a>,
    diagnostics: Vec<(DiagnosticKind, Range)>,
    extend_immutable_calls: Vec<CallPath<'a>>,
}

impl<'a, 'b> Visitor<'b> for ArgumentDefaultVisitor<'b>
where
    'b: 'a,
{
    fn visit_expr(&mut self, expr: &'b Expr) {
        match &expr.node {
            ExprKind::Call { func, args, .. } => {
                if !is_mutable_func(self.checker, func)
                    && !is_immutable_func(self.checker, func, &self.extend_immutable_calls)
                    && !is_nan_or_infinity(func, args)
                {
                    self.diagnostics.push((
                        FunctionCallInDefaultArgument {
                            name: compose_call_path(func),
                        }
                        .into(),
                        Range::from(expr),
                    ));
                }
                visitor::walk_expr(self, expr);
            }
            ExprKind::Lambda { .. } => {}
            _ => visitor::walk_expr(self, expr),
        }
    }
}

fn is_nan_or_infinity(expr: &Expr, args: &[Expr]) -> bool {
    let ExprKind::Name { id, .. } = &expr.node else {
        return false;
    };
    if id != "float" {
        return false;
    }
    let Some(arg) = args.first() else {
        return false;
    };
    let ExprKind::Constant {
        value: Constant::Str(value),
        ..
    } = &arg.node else {
        return false;
    };
    let lowercased = value.to_lowercase();
    matches!(
        lowercased.as_str(),
        "nan" | "+nan" | "-nan" | "inf" | "+inf" | "-inf" | "infinity" | "+infinity" | "-infinity"
    )
}

/// B008
pub fn function_call_argument_default(checker: &mut Checker, arguments: &Arguments) {
    // Map immutable calls to (module, member) format.
    let extend_immutable_calls: Vec<CallPath> = checker
        .settings
        .flake8_bugbear
        .extend_immutable_calls
        .iter()
        .map(|target| from_qualified_name(target))
        .collect();
    let diagnostics = {
        let mut visitor = ArgumentDefaultVisitor {
            checker,
            diagnostics: vec![],
            extend_immutable_calls,
        };
        for expr in arguments
            .defaults
            .iter()
            .chain(arguments.kw_defaults.iter())
        {
            visitor.visit_expr(expr);
        }
        visitor.diagnostics
    };
    for (check, range) in diagnostics {
        checker.diagnostics.push(Diagnostic::new(check, range));
    }
}
