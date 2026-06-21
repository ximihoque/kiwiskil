require 'json'
require_relative 'helper'

# Greeter provides greeting helpers.
module Greeter
  # Says hello to the given name.
  def self.hello(name)
    puts name
  end
end

# Widget counts things.
class Widget
  # Increments the counter by n.
  def bump(n)
    helper(n)
  end
end

# Top-level utility function.
def top_level
  42
end
