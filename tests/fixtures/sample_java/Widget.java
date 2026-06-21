package com.example;

import java.util.List;
import java.util.ArrayList;

/** A small widget that counts things. */
public class Widget {
    private int count;

    /** Increments the counter by n and returns the result. */
    public int bump(int n) {
        return helper(n);
    }

    static int helper(int x) {
        return x + 1;
    }
}
