package bridge

import (
	"encoding/json"
	"io/ioutil"
	"os"
)

type Blockheight struct {
	LastHeight    uint64 `json:"lastHeight"`
	StellarCursor string `json:"stellarCursor"`
}

type BlockPersistency struct {
	location string
}

func initPersist(location string) (*BlockPersistency, error) {
	return &BlockPersistency{
		location: location,
	}, nil
}

func (b *BlockPersistency) saveHeight(height uint64) error {
	blockheight, err := b.GetHeight()
	if err != nil {
		return err
	}

	blockheight.LastHeight = height
	return b.Save(blockheight)
}

func (b *BlockPersistency) saveStellarCursor(cursor string) error {
	blockheight, err := b.GetHeight()
	if err != nil {
		return err
	}

	blockheight.StellarCursor = cursor
	return b.Save(blockheight)
}

func (b *BlockPersistency) GetHeight() (*Blockheight, error) {
	var blockheight Blockheight
	file, err := ioutil.ReadFile(b.location)
	if os.IsNotExist(err) {
		return &blockheight, nil
	}
	if err != nil {
		return nil, err
	}
	err = json.Unmarshal(file, &blockheight)
	if err != nil {
		return nil, err
	}

	return &blockheight, nil
}

func (b *BlockPersistency) Save(blockheight *Blockheight) error {
	updatedPersistency, err := json.Marshal(blockheight)
	if err != nil {
		return err
	}

	return ioutil.WriteFile(b.location, updatedPersistency, 0644)
}
