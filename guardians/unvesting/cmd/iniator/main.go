package main

import (
	"context"
	"flag"
	"log"
	"time"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/signer"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/price"
)

func main() {
	var network string

	flag.StringVar(&network, "network", "public", "The stellar network to use: 'public' or 'test'")

	flag.Parse()

	if network != "public" && network != "test" {
		flag.Usage()
		log.Fatalln("Invalid network")
	}
	log.Println("Starting initiator on the", network, "network")
	montlyPrices := []price.MonthlyPrice{}
	calculationDate := time.Date(2021, 5, 1, 0, 0, 0, 0, time.UTC)
	for calculationDate.Before(time.Now()) {
		monthlyPrice, err := price.GetMontlyPrice(calculationDate.Month(), calculationDate.Year())
		if err != nil {
			log.Println("ERROR getting the montly price for ", calculationDate.Month(), calculationDate.Year(), err)
		}
		montlyPrices = append(montlyPrices, monthlyPrice)
		log.Println(monthlyPrice.Month, calculationDate.Year(), "Price:", monthlyPrice.Price)
		calculationDate = calculationDate.AddDate(0, 1, 0)
	}

	rootCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	connMgr := communication.NewConnectionManager()
	communicationCtx, cancel := context.WithCancel(rootCtx)
	defer cancel()
	connMgr.Start(communicationCtx, nil)
	signerAddresses := signer.GetSignerAddresses(network)
	for _, signerAddress := range signerAddresses {
		err := connMgr.ConnectTo(signerAddress)
		if err != nil {
			log.Println("Failed to connect to signer", signerAddress, err)
		} else {
			log.Println("Connected to signer", signerAddress)
		}
	}
	signerClient := signer.NewSigningClient(connMgr.Host)
	for {
		//Check the status of the signers every 10 minutes
		for _, signerAddress := range signerAddresses {
			statusMessage, err := signerClient.CallGetStatus(signerAddress)
			if err != nil {
				log.Println("ERROR calling GetStatus for signer", signerAddress, ":", err)
			} else {
				log.Println("Status of", signerAddress, ":", statusMessage)
			}
		}
		time.Sleep(time.Minute * 10)
	}
}
