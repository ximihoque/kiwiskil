use std::fmt;

/// A widget struct that counts things.
pub struct Widget {
    count: i32,
}

impl Widget {
    /// Bumps the count by n and returns it.
    pub fn bump(&self, n: i32) -> i32 {
        helper(n)
    }
}

/// Greets the given name.
pub fn greet(name: &str) -> String {
    String::from(name)
}

trait Speak {
    fn speak(&self);
}
