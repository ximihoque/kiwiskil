package main

import (
	"fmt"
	"net/http"
)

// Greet returns a friendly greeting for the given name.
func Greet(name string) string {
	fmt.Println(name)
	return "hi " + name
}

// Server holds the listen address.
type Server struct {
	addr string
}

// Start launches the HTTP server.
func (s *Server) Start() error {
	Greet(s.addr)
	http.ListenAndServe(s.addr, nil)
	return nil
}
