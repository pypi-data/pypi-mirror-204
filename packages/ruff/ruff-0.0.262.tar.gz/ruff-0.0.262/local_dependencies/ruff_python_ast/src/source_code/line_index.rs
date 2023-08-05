use ruff_text_size::{TextLen, TextRange, TextSize};
use rustpython_parser::ast::Location;
use std::fmt;
use std::fmt::{Debug, Formatter};
use std::num::NonZeroUsize;
use std::ops::Deref;
use std::sync::Arc;

/// Index for fast [`Location`] to [byte offset](TextSize) conversions.
///
/// Cloning a [`LineIndex`] is cheap because it only requires bumping a reference count.
#[derive(Clone)]
pub struct LineIndex {
    inner: Arc<LineIndexInner>,
}

struct LineIndexInner {
    line_starts: Vec<TextSize>,
    kind: IndexKind,
}

impl LineIndex {
    /// Builds the [`LineIndex`] from the source text of a file.
    pub fn from_source_text(text: &str) -> Self {
        assert!(u32::try_from(text.len()).is_ok());

        let mut line_starts: Vec<TextSize> = Vec::with_capacity(text.len() / 88);
        line_starts.push(TextSize::default());

        let bytes = text.as_bytes();
        let mut utf8 = false;

        for (i, byte) in bytes.iter().enumerate() {
            utf8 |= !byte.is_ascii();

            match byte {
                // Only track one line break for `\r\n`.
                b'\r' if bytes.get(i + 1) == Some(&b'\n') => continue,
                b'\n' | b'\r' => {
                    line_starts.push(TextSize::try_from(i + 1).unwrap());
                }
                _ => {}
            }
        }

        let kind = if utf8 {
            IndexKind::Utf8
        } else {
            IndexKind::Ascii
        };

        Self {
            inner: Arc::new(LineIndexInner { line_starts, kind }),
        }
    }

    fn kind(&self) -> IndexKind {
        self.inner.kind
    }

    /// Converts a [`Location`] to it's [byte offset](TextSize) in the source code.
    pub fn location_offset(&self, location: Location, contents: &str) -> TextSize {
        let line_index = OneIndexed::new(location.row()).unwrap();
        let line_range = self.line_range(line_index, contents);

        let column_offset = match self.kind() {
            IndexKind::Ascii => TextSize::try_from(location.column()).unwrap(),
            IndexKind::Utf8 => {
                let line = &contents[line_range];

                // Skip the bom character
                let bom_len =
                    usize::from(line_index.to_zero_indexed() == 0 && line.starts_with('\u{feff}'));

                match line.char_indices().nth(location.column() + bom_len) {
                    Some((offset, _)) => TextSize::try_from(offset).unwrap(),
                    None => line_range.len(),
                }
            }
        };

        line_range.start() + column_offset
    }

    /// Return the number of lines in the source code.
    pub(crate) fn line_count(&self) -> usize {
        self.line_starts().len()
    }

    /// Returns the [byte offset](TextSize) for the `line` with the given index.
    pub(crate) fn line_start(&self, line: OneIndexed, contents: &str) -> TextSize {
        let row_index = line.to_zero_indexed();
        let starts = self.line_starts();

        // If start-of-line position after last line
        if row_index == starts.len() {
            contents.text_len()
        } else {
            starts[row_index]
        }
    }

    /// Returns the [byte offset](TextSize) of the `line`'s end.
    /// The offset is the end of the line, up to and including the newline character ending the line (if any).
    pub(crate) fn line_end(&self, line: OneIndexed, contents: &str) -> TextSize {
        let row_index = line.to_zero_indexed();
        let starts = self.line_starts();

        // If start-of-line position after last line
        if row_index.saturating_add(1) >= starts.len() {
            contents.text_len()
        } else {
            starts[row_index + 1]
        }
    }

    /// Returns the [`TextRange`] of the `line` with the given index.
    /// The start points to the first character's [byte offset](TextSize), the end up to, and including
    /// the newline character ending the line (if any).
    pub(crate) fn line_range(&self, line: OneIndexed, contents: &str) -> TextRange {
        let starts = self.line_starts();

        if starts.len() == line.to_zero_indexed() {
            TextRange::empty(contents.text_len())
        } else {
            TextRange::new(
                self.line_start(line, contents),
                self.line_start(line.saturating_add(1), contents),
            )
        }
    }

    /// Returns the [byte offsets](TextSize) for every line
    pub fn line_starts(&self) -> &[TextSize] {
        &self.inner.line_starts
    }
}

impl Deref for LineIndex {
    type Target = [TextSize];

    fn deref(&self) -> &Self::Target {
        self.line_starts()
    }
}

impl Debug for LineIndex {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.debug_list().entries(self.line_starts()).finish()
    }
}

#[derive(Debug, Clone, Copy)]
enum IndexKind {
    /// Optimized index for an ASCII only document
    Ascii,

    /// Index for UTF8 documents
    Utf8,
}

/// Type-safe wrapper for a value whose logical range starts at `1`, for
/// instance the line or column numbers in a file
///
/// Internally this is represented as a [`NonZeroUsize`], this enables some
/// memory optimizations
#[derive(Debug, Copy, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct OneIndexed(NonZeroUsize);

impl OneIndexed {
    // SAFETY: These constants are being initialized with non-zero values
    /// The smallest value that can be represented by this integer type.
    pub const MIN: Self = unwrap(Self::new(1));
    /// The largest value that can be represented by this integer type
    pub const MAX: Self = unwrap(Self::new(usize::MAX));

    pub const ONE: NonZeroUsize = unwrap(NonZeroUsize::new(1));

    /// Creates a non-zero if the given value is not zero.
    pub const fn new(value: usize) -> Option<Self> {
        match NonZeroUsize::new(value) {
            Some(value) => Some(Self(value)),
            None => None,
        }
    }

    /// Construct a new [`OneIndexed`] from a zero-indexed value
    pub const fn from_zero_indexed(value: usize) -> Self {
        Self(Self::ONE.saturating_add(value))
    }

    /// Returns the value as a primitive type.
    pub const fn get(self) -> usize {
        self.0.get()
    }

    /// Return the zero-indexed primitive value for this [`OneIndexed`]
    pub const fn to_zero_indexed(self) -> usize {
        self.0.get() - 1
    }

    /// Saturating integer addition. Computes `self + rhs`, saturating at
    /// the numeric bounds instead of overflowing.
    #[must_use]
    pub const fn saturating_add(self, rhs: usize) -> Self {
        match NonZeroUsize::new(self.0.get().saturating_add(rhs)) {
            Some(value) => Self(value),
            None => Self::MAX,
        }
    }

    /// Saturating integer subtraction. Computes `self - rhs`, saturating
    /// at the numeric bounds instead of overflowing.
    #[must_use]
    pub const fn saturating_sub(self, rhs: usize) -> Self {
        match NonZeroUsize::new(self.0.get().saturating_sub(rhs)) {
            Some(value) => Self(value),
            None => Self::MIN,
        }
    }
}

impl std::fmt::Display for OneIndexed {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        std::fmt::Debug::fmt(&self.0.get(), f)
    }
}

/// A const `Option::unwrap` without nightly features:
/// [Tracking issue](https://github.com/rust-lang/rust/issues/67441)
const fn unwrap<T: Copy>(option: Option<T>) -> T {
    match option {
        Some(value) => value,
        None => panic!("unwrapping None"),
    }
}

#[cfg(test)]
mod tests {
    use crate::source_code::line_index::LineIndex;
    use ruff_text_size::TextSize;
    use rustpython_parser::ast::Location;

    #[test]
    fn ascii_index() {
        let index = LineIndex::from_source_text("");
        assert_eq!(index.line_starts(), &[TextSize::from(0)]);

        let index = LineIndex::from_source_text("x = 1");
        assert_eq!(index.line_starts(), &[TextSize::from(0)]);

        let index = LineIndex::from_source_text("x = 1\n");
        assert_eq!(index.line_starts(), &[TextSize::from(0), TextSize::from(6)]);

        let index = LineIndex::from_source_text("x = 1\ny = 2\nz = x + y\n");
        assert_eq!(
            index.line_starts(),
            &[
                TextSize::from(0),
                TextSize::from(6),
                TextSize::from(12),
                TextSize::from(22)
            ]
        );
    }

    #[test]
    fn ascii_byte_offset() {
        let contents = "x = 1\ny = 2";
        let index = LineIndex::from_source_text(contents);

        // First row.
        let loc = index.location_offset(Location::new(1, 0), contents);
        assert_eq!(loc, TextSize::from(0));

        // Second row.
        let loc = index.location_offset(Location::new(2, 0), contents);
        assert_eq!(loc, TextSize::from(6));

        // One-past-the-end.
        let loc = index.location_offset(Location::new(3, 0), contents);
        assert_eq!(loc, TextSize::from(11));
    }

    #[test]
    fn ascii_carriage_return() {
        let contents = "x = 4\ry = 3";
        let index = LineIndex::from_source_text(contents);
        assert_eq!(index.line_starts(), &[TextSize::from(0), TextSize::from(6)]);

        assert_eq!(
            index.location_offset(Location::new(1, 4), contents),
            TextSize::from(4)
        );
        assert_eq!(
            index.location_offset(Location::new(2, 0), contents),
            TextSize::from(6)
        );
        assert_eq!(
            index.location_offset(Location::new(2, 1), contents),
            TextSize::from(7)
        );
    }

    #[test]
    fn ascii_carriage_return_newline() {
        let contents = "x = 4\r\ny = 3";
        let index = LineIndex::from_source_text(contents);
        assert_eq!(index.line_starts(), &[TextSize::from(0), TextSize::from(7)]);

        assert_eq!(
            index.location_offset(Location::new(1, 4), contents),
            TextSize::from(4)
        );
        assert_eq!(
            index.location_offset(Location::new(2, 0), contents),
            TextSize::from(7)
        );
        assert_eq!(
            index.location_offset(Location::new(2, 1), contents),
            TextSize::from(8)
        );
    }

    #[test]
    fn utf8_index() {
        let index = LineIndex::from_source_text("x = '🫣'");
        assert_eq!(index.line_count(), 1);
        assert_eq!(index.line_starts(), &[TextSize::from(0)]);

        let index = LineIndex::from_source_text("x = '🫣'\n");
        assert_eq!(index.line_count(), 2);
        assert_eq!(
            index.line_starts(),
            &[TextSize::from(0), TextSize::from(11)]
        );

        let index = LineIndex::from_source_text("x = '🫣'\ny = 2\nz = x + y\n");
        assert_eq!(index.line_count(), 4);
        assert_eq!(
            index.line_starts(),
            &[
                TextSize::from(0),
                TextSize::from(11),
                TextSize::from(17),
                TextSize::from(27)
            ]
        );

        let index = LineIndex::from_source_text("# 🫣\nclass Foo:\n    \"\"\".\"\"\"");
        assert_eq!(index.line_count(), 3);
        assert_eq!(
            index.line_starts(),
            &[TextSize::from(0), TextSize::from(7), TextSize::from(18)]
        );
    }

    #[test]
    fn utf8_carriage_return() {
        let contents = "x = '🫣'\ry = 3";
        let index = LineIndex::from_source_text(contents);
        assert_eq!(index.line_count(), 2);
        assert_eq!(
            index.line_starts(),
            &[TextSize::from(0), TextSize::from(11)]
        );

        // Second '
        assert_eq!(
            index.location_offset(Location::new(1, 6), contents),
            TextSize::from(9)
        );
        assert_eq!(
            index.location_offset(Location::new(2, 0), contents),
            TextSize::from(11)
        );
        assert_eq!(
            index.location_offset(Location::new(2, 1), contents),
            TextSize::from(12)
        );
    }

    #[test]
    fn utf8_carriage_return_newline() {
        let contents = "x = '🫣'\r\ny = 3";
        let index = LineIndex::from_source_text(contents);
        assert_eq!(index.line_count(), 2);
        assert_eq!(
            index.line_starts(),
            &[TextSize::from(0), TextSize::from(12)]
        );

        // Second '
        assert_eq!(
            index.location_offset(Location::new(1, 6), contents),
            TextSize::from(9)
        );
        assert_eq!(
            index.location_offset(Location::new(2, 0), contents),
            TextSize::from(12)
        );
        assert_eq!(
            index.location_offset(Location::new(2, 1), contents),
            TextSize::from(13)
        );
    }

    #[test]
    fn utf8_byte_offset() {
        let contents = "x = '☃'\ny = 2";
        let index = LineIndex::from_source_text(contents);
        assert_eq!(
            index.line_starts(),
            &[TextSize::from(0), TextSize::from(10)]
        );

        // First row.
        let loc = index.location_offset(Location::new(1, 0), contents);
        assert_eq!(loc, TextSize::from(0));

        let loc = index.location_offset(Location::new(1, 5), contents);
        assert_eq!(loc, TextSize::from(5));
        assert_eq!(&"x = '☃'\ny = 2"[usize::from(loc)..], "☃'\ny = 2");

        let loc = index.location_offset(Location::new(1, 6), contents);
        assert_eq!(loc, TextSize::from(8));
        assert_eq!(&"x = '☃'\ny = 2"[usize::from(loc)..], "'\ny = 2");

        // Second row.
        let loc = index.location_offset(Location::new(2, 0), contents);
        assert_eq!(loc, TextSize::from(10));

        // One-past-the-end.
        let loc = index.location_offset(Location::new(3, 0), contents);
        assert_eq!(loc, TextSize::from(15));
    }
}
