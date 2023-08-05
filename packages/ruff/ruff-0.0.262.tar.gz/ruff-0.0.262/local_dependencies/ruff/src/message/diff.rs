use crate::message::Message;
use colored::{Color, ColoredString, Colorize, Styles};
use ruff_diagnostics::Fix;
use ruff_python_ast::source_code::{OneIndexed, SourceCode};
use ruff_python_ast::types::Range;
use ruff_text_size::{TextRange, TextSize};
use similar::{ChangeTag, TextDiff};
use std::fmt::{Display, Formatter};
use std::num::NonZeroUsize;

/// Renders a diff that shows the code fixes.
///
/// The implementation isn't fully fledged out and only used by tests. Before using in production, try
/// * Improve layout
/// * Replace tabs with spaces for a consistent experience across terminals
/// * Replace zero-width whitespaces
/// * Print a simpler diff if only a single line has changed
/// * Compute the diff from the [`Edit`] because diff calculation is expensive.
pub(super) struct Diff<'a> {
    fix: &'a Fix,
    source_code: SourceCode<'a, 'a>,
}

impl<'a> Diff<'a> {
    pub fn from_message(message: &'a Message) -> Option<Diff> {
        match message.file.source_code() {
            Some(source_code) if !message.fix.is_empty() => Some(Diff {
                source_code,
                fix: &message.fix,
            }),
            _ => None,
        }
    }
}

impl Display for Diff<'_> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let mut output = String::with_capacity(self.source_code.text().len());
        let mut last_end = TextSize::default();

        for edit in self.fix.edits() {
            let edit_range = self
                .source_code
                .text_range(Range::new(edit.location(), edit.end_location()));
            output.push_str(&self.source_code.text()[TextRange::new(last_end, edit_range.start())]);
            output.push_str(edit.content().unwrap_or_default());
            last_end = edit_range.end();
        }

        output.push_str(&self.source_code.text()[usize::from(last_end)..]);

        let diff = TextDiff::from_lines(self.source_code.text(), &output);

        writeln!(f, "{}", "ℹ Suggested fix".blue())?;

        let (largest_old, largest_new) = diff
            .ops()
            .last()
            .map(|op| (op.old_range().start, op.new_range().start))
            .unwrap_or_default();

        let digit_with =
            calculate_print_width(OneIndexed::from_zero_indexed(largest_new.max(largest_old)));

        for (idx, group) in diff.grouped_ops(3).iter().enumerate() {
            if idx > 0 {
                writeln!(f, "{:-^1$}", "-", 80)?;
            }
            for op in group {
                for change in diff.iter_inline_changes(op) {
                    let sign = match change.tag() {
                        ChangeTag::Delete => "-",
                        ChangeTag::Insert => "+",
                        ChangeTag::Equal => " ",
                    };

                    let line_style = LineStyle::from(change.tag());

                    let old_index = change.old_index().map(OneIndexed::from_zero_indexed);
                    let new_index = change.new_index().map(OneIndexed::from_zero_indexed);

                    write!(
                        f,
                        "{} {} |{}",
                        Line {
                            index: old_index,
                            width: digit_with
                        },
                        Line {
                            index: new_index,
                            width: digit_with
                        },
                        line_style.apply_to(sign).bold()
                    )?;

                    for (emphasized, value) in change.iter_strings_lossy() {
                        if emphasized {
                            write!(f, "{}", line_style.apply_to(&value).underline().on_black())?;
                        } else {
                            write!(f, "{}", line_style.apply_to(&value))?;
                        }
                    }
                    if change.missing_newline() {
                        writeln!(f)?;
                    }
                }
            }
        }

        Ok(())
    }
}

struct LineStyle {
    fgcolor: Option<Color>,
    style: Option<Styles>,
}

impl LineStyle {
    fn apply_to(&self, input: &str) -> ColoredString {
        let mut colored = ColoredString::from(input);
        if let Some(color) = self.fgcolor {
            colored = colored.color(color);
        }

        if let Some(style) = self.style {
            match style {
                Styles::Clear => colored.clear(),
                Styles::Bold => colored.bold(),
                Styles::Dimmed => colored.dimmed(),
                Styles::Underline => colored.underline(),
                Styles::Reversed => colored.reversed(),
                Styles::Italic => colored.italic(),
                Styles::Blink => colored.blink(),
                Styles::Hidden => colored.hidden(),
                Styles::Strikethrough => colored.strikethrough(),
            }
        } else {
            colored
        }
    }
}

impl From<ChangeTag> for LineStyle {
    fn from(value: ChangeTag) -> Self {
        match value {
            ChangeTag::Equal => LineStyle {
                fgcolor: None,
                style: Some(Styles::Dimmed),
            },
            ChangeTag::Delete => LineStyle {
                fgcolor: Some(Color::Red),
                style: None,
            },
            ChangeTag::Insert => LineStyle {
                fgcolor: Some(Color::Green),
                style: None,
            },
        }
    }
}

struct Line {
    index: Option<OneIndexed>,
    width: NonZeroUsize,
}

impl Display for Line {
    fn fmt(&self, f: &mut Formatter) -> std::fmt::Result {
        match self.index {
            None => {
                for _ in 0..self.width.get() {
                    f.write_str(" ")?;
                }
                Ok(())
            }
            Some(idx) => write!(f, "{:<width$}", idx, width = self.width.get()),
        }
    }
}

/// Calculate the length of the string representation of `value`
pub(super) fn calculate_print_width(mut value: OneIndexed) -> NonZeroUsize {
    const TEN: OneIndexed = OneIndexed::from_zero_indexed(9);

    let mut width = OneIndexed::ONE;

    while value >= TEN {
        value = OneIndexed::new(value.get() / 10).unwrap_or(OneIndexed::MIN);
        width = width.checked_add(1).unwrap();
    }

    width
}
