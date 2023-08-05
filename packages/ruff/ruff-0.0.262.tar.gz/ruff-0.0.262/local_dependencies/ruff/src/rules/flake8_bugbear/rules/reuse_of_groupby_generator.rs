use rustpython_parser::ast::{Comprehension, Expr, ExprKind, Stmt, StmtKind};

use ruff_diagnostics::{Diagnostic, Violation};
use ruff_macros::{derive_message_formats, violation};
use ruff_python_ast::types::Range;
use ruff_python_ast::visitor::{self, Visitor};

use crate::checkers::ast::Checker;

/// ## What it does
/// Checks for multiple usage of the generator returned from
/// `itertools.groupby()`.
///
/// ## Why is it bad?
/// Using the generator more than once will do nothing on the second usage.
/// If that data is needed later, it should be stored as a list.
///
/// ## Examples:
/// ```python
/// import itertools
///
/// for name, group in itertools.groupby(data):
///     for _ in range(5):
///         do_something_with_the_group(group)
/// ```
///
/// Use instead:
/// ```python
/// import itertools
///
/// for name, group in itertools.groupby(data):
///     values = list(group)
///     for _ in range(5):
///         do_something_with_the_group(values)
/// ```
#[violation]
pub struct ReuseOfGroupbyGenerator;

impl Violation for ReuseOfGroupbyGenerator {
    #[derive_message_formats]
    fn message(&self) -> String {
        format!("Using the generator returned from `itertools.groupby()` more than once will do nothing on the second usage")
    }
}

/// A [`Visitor`] that collects all the usage of `group_name` in the body of
/// a `for` loop.
struct GroupNameFinder<'a> {
    /// Variable name for the group.
    group_name: &'a str,
    /// Number of times the `group_name` variable was seen during the visit.
    usage_count: u32,
    /// A flag indicating that the visitor is inside a nested `for` or `while`
    /// loop or inside a `dict`, `list` or `set` comprehension.
    nested: bool,
    /// A flag indicating that the `group_name` variable has been overridden
    /// during the visit.
    overridden: bool,
    /// A stack of `if` statements.
    parent_ifs: Vec<&'a Stmt>,
    /// A stack of counters where each counter is itself a list of usage count.
    /// This is used specifically for mutually exclusive statements such as an
    /// `if` or `match`.
    ///
    /// The stack element represents an entire `if` or `match` statement while
    /// the number inside the element represents the usage count for one of
    /// the branches of the statement. The order of the count corresponds the
    /// branch order.
    counter_stack: Vec<Vec<u32>>,
    /// A list of reused expressions.
    exprs: Vec<&'a Expr>,
}

impl<'a> GroupNameFinder<'a> {
    fn new(group_name: &'a str) -> Self {
        GroupNameFinder {
            group_name,
            usage_count: 0,
            nested: false,
            overridden: false,
            parent_ifs: Vec::new(),
            counter_stack: Vec::new(),
            exprs: Vec::new(),
        }
    }

    fn name_matches(&self, expr: &Expr) -> bool {
        if let ExprKind::Name { id, .. } = &expr.node {
            id == self.group_name
        } else {
            false
        }
    }
}

impl<'a, 'b> Visitor<'b> for GroupNameFinder<'a>
where
    'b: 'a,
{
    fn visit_stmt(&mut self, stmt: &'a Stmt) {
        if self.overridden {
            return;
        }
        match &stmt.node {
            StmtKind::For {
                target, iter, body, ..
            } => {
                if self.name_matches(target) {
                    self.overridden = true;
                } else {
                    if self.name_matches(iter) {
                        self.usage_count += 1;
                        // This could happen when the group is being looped
                        // over multiple times:
                        //      for item in group:
                        //          ...
                        //
                        //      # Group is being reused here
                        //      for item in group:
                        //          ...
                        if self.usage_count > 1 {
                            self.exprs.push(iter);
                        }
                    }
                    self.nested = true;
                    visitor::walk_body(self, body);
                    self.nested = false;
                }
            }
            StmtKind::While { body, .. } => {
                self.nested = true;
                visitor::walk_body(self, body);
                self.nested = false;
            }
            StmtKind::If { test, body, orelse } => {
                // Determine whether we're on an `if` arm (as opposed to an `elif`).
                let is_if_arm = !self.parent_ifs.iter().any(|parent| {
                    if let StmtKind::If { orelse, .. } = &parent.node {
                        orelse.len() == 1 && &orelse[0] == stmt
                    } else {
                        false
                    }
                });

                if is_if_arm {
                    // Initialize the vector with the count for current branch.
                    self.counter_stack.push(vec![0]);
                } else {
                    // SAFETY: `unwrap` is safe because we're either in `elif` or
                    // `else` branch which can come only after an `if` branch.
                    // When inside an `if` branch, a new vector will be pushed
                    // onto the stack.
                    self.counter_stack.last_mut().unwrap().push(0);
                }

                let has_else = orelse
                    .first()
                    .map_or(false, |expr| !matches!(expr.node, StmtKind::If { .. }));

                self.parent_ifs.push(stmt);
                if has_else {
                    // There's no `StmtKind::Else`; instead, the `else` contents are directly on
                    // the `orelse` of the `StmtKind::If` node. We want to add a new counter for
                    // the `orelse` branch, but first, we need to visit the `if` body manually.
                    self.visit_expr(test);
                    self.visit_body(body);

                    // Now, we're in an `else` block.
                    self.counter_stack.last_mut().unwrap().push(0);
                    self.visit_body(orelse);
                } else {
                    visitor::walk_stmt(self, stmt);
                }
                self.parent_ifs.pop();

                if is_if_arm {
                    if let Some(last) = self.counter_stack.pop() {
                        // This is the max number of group usage from all the
                        // branches of this `if` statement.
                        let max_count = last.into_iter().max().unwrap_or(0);
                        if let Some(current_last) = self.counter_stack.last_mut() {
                            *current_last.last_mut().unwrap() += max_count;
                        } else {
                            self.usage_count += max_count;
                        }
                    }
                }
            }
            StmtKind::Match { subject, cases } => {
                self.counter_stack.push(Vec::with_capacity(cases.len()));
                self.visit_expr(subject);
                for match_case in cases {
                    self.counter_stack.last_mut().unwrap().push(0);
                    self.visit_match_case(match_case);
                }
                if let Some(last) = self.counter_stack.pop() {
                    // This is the max number of group usage from all the
                    // branches of this `match` statement.
                    let max_count = last.into_iter().max().unwrap_or(0);
                    if let Some(current_last) = self.counter_stack.last_mut() {
                        *current_last.last_mut().unwrap() += max_count;
                    } else {
                        self.usage_count += max_count;
                    }
                }
            }
            StmtKind::Assign { targets, value, .. } => {
                if targets.iter().any(|target| self.name_matches(target)) {
                    self.overridden = true;
                } else {
                    self.visit_expr(value);
                }
            }
            StmtKind::AnnAssign { target, value, .. } => {
                if self.name_matches(target) {
                    self.overridden = true;
                } else if let Some(expr) = value {
                    self.visit_expr(expr);
                }
            }
            _ => visitor::walk_stmt(self, stmt),
        }
    }

    fn visit_comprehension(&mut self, comprehension: &'a Comprehension) {
        if self.name_matches(&comprehension.target) {
            self.overridden = true;
        }
        if self.overridden {
            return;
        }
        if self.name_matches(&comprehension.iter) {
            self.usage_count += 1;
            if self.usage_count > 1 {
                self.exprs.push(&comprehension.iter);
            }
        }
    }

    fn visit_expr(&mut self, expr: &'a Expr) {
        if let ExprKind::NamedExpr { target, .. } = &expr.node {
            if self.name_matches(target) {
                self.overridden = true;
            }
        }
        if self.overridden {
            return;
        }

        match &expr.node {
            ExprKind::ListComp { elt, generators } | ExprKind::SetComp { elt, generators } => {
                for comprehension in generators {
                    self.visit_comprehension(comprehension);
                }
                if !self.overridden {
                    self.nested = true;
                    visitor::walk_expr(self, elt);
                    self.nested = false;
                }
            }
            ExprKind::DictComp {
                key,
                value,
                generators,
            } => {
                for comprehension in generators {
                    self.visit_comprehension(comprehension);
                }
                if !self.overridden {
                    self.nested = true;
                    visitor::walk_expr(self, key);
                    visitor::walk_expr(self, value);
                    self.nested = false;
                }
            }
            _ => {
                if self.name_matches(expr) {
                    // If the stack isn't empty, then we're in one of the branches of
                    // a mutually exclusive statement. Otherwise, we'll add it to the
                    // global count.
                    if let Some(last) = self.counter_stack.last_mut() {
                        *last.last_mut().unwrap() += 1;
                    } else {
                        self.usage_count += 1;
                    }

                    let current_usage_count = self.usage_count
                        + self
                            .counter_stack
                            .iter()
                            .map(|count| count.last().unwrap_or(&0))
                            .sum::<u32>();

                    // For nested loops, the variable usage could be once but the
                    // loop makes it being used multiple times.
                    if self.nested || current_usage_count > 1 {
                        self.exprs.push(expr);
                    }
                } else {
                    visitor::walk_expr(self, expr);
                }
            }
        }
    }
}

/// B031
pub fn reuse_of_groupby_generator(
    checker: &mut Checker,
    target: &Expr,
    body: &[Stmt],
    iter: &Expr,
) {
    let ExprKind::Call { func, .. } = &iter.node else {
        return;
    };
    let ExprKind::Tuple { elts, .. } = &target.node else {
        // Ignore any `groupby()` invocation that isn't unpacked
        return;
    };
    if elts.len() != 2 {
        return;
    }
    // We have an invocation of groupby which is a simple unpacking
    let ExprKind::Name { id: group_name, .. } = &elts[1].node else {
        return;
    };
    // Check if the function call is `itertools.groupby`
    if !checker
        .ctx
        .resolve_call_path(func)
        .map_or(false, |call_path| {
            call_path.as_slice() == ["itertools", "groupby"]
        })
    {
        return;
    }
    let mut finder = GroupNameFinder::new(group_name);
    for stmt in body.iter() {
        finder.visit_stmt(stmt);
    }
    for expr in finder.exprs {
        checker
            .diagnostics
            .push(Diagnostic::new(ReuseOfGroupbyGenerator, Range::from(expr)));
    }
}
