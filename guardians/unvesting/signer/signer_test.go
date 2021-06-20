package signer

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSigningServiceGetStatus(t *testing.T) {
	s := NewSigningService("test")
	request := GetStatusRequest{}
	reply := GetStatusResponse{}
	err := s.GetStatus(context.Background(), request, &reply)
	assert.NoError(t, err)
	assert.Equal(t, "Alive and kicking", reply.Message)
}
