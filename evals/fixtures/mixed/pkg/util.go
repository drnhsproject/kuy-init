package pkg

type Server struct{}

func (s *Server) Start(port int) error { return nil }

func NewServer() *Server { return nil }
