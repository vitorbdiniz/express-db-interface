package main

import (
	"bytes"
	"crypto/rand"
	"encoding/base32"
	"io/ioutil"

	"github.com/xtgo/uuid"
)

var encoding = base32.NewEncoding("ybndrfg8ejkmcpqxot1uwisza345h769")

func main() {
	Id := NewBytesId(false, 25)
	ioutil.WriteFile("./main/generator/go_scripts/id.txt", Id, 0644)
}

func NewBytesId(isId bool, length int) []byte {
	var b bytes.Buffer
	var bytes []byte
	encoder := base32.NewEncoder(encoding, &b)
	if isId {
		uuID := uuid.NewRandom()
		encoder.Write(uuID.Bytes())
		b.Truncate(26) // removes the '==' padding
	} else {
		bytes = make([]byte, length)
		rand.Read(bytes)
		encoder.Write(bytes)
		b.Truncate(length)
	}
	encoder.Close()
	return b.Bytes()
}
