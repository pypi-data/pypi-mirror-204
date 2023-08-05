//! Checks for `++n`.
//!
//! ## Why is this bad?
//!
//! Python does not support the unary prefix increment. Writing `++n` is
//! equivalent to `+(+(n))`, which equals `n`.
//!
//! ## Example
//!
//! ```python
//! ++n;
//! ```
//!
//! Use instead:
//!
//! ```python
//! n += 1
//! ```

use rustpython_parser::ast::{Expr, ExprKind, Unaryop};

use ruff_diagnostics::{Diagnostic, Violation};
use ruff_macros::{derive_message_formats, violation};
use ruff_python_ast::types::Range;

use crate::checkers::ast::Checker;

#[violation]
pub struct UnaryPrefixIncrement;

impl Violation for UnaryPrefixIncrement {
    #[derive_message_formats]
    fn message(&self) -> String {
        format!("Python does not support the unary prefix increment")
    }
}

/// B002
pub fn unary_prefix_increment(checker: &mut Checker, expr: &Expr, op: &Unaryop, operand: &Expr) {
    if !matches!(op, Unaryop::UAdd) {
        return;
    }
    let ExprKind::UnaryOp { op, .. } = &operand.node else {
            return;
        };
    if !matches!(op, Unaryop::UAdd) {
        return;
    }
    checker
        .diagnostics
        .push(Diagnostic::new(UnaryPrefixIncrement, Range::from(expr)));
}
