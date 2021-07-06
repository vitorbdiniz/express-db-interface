package main

import (
	"time"
)

func main() int64 {
	return time.Now().UnixNano() / int64(time.Millisecond)
}

func GetMillis() int64 {
	return time.Now().UnixNano() / int64(time.Millisecond)
}
