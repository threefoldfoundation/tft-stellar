package price

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"time"
)

// MontlyPrice Is a Price in USD for a specific month
type MonthlyPrice struct {
	Month time.Month
	Year  int
	Price float64
}

type xlmPrice struct {
	timestamp int64
	price     float64
}

func unmarshalXLMPricesJSON(bs []byte) (xlmPrices []xlmPrice, err error) {
	arr := [][]float64{}
	err = json.Unmarshal(bs, &arr)
	if err != nil {
		return
	}
	xlmPrices = make([]xlmPrice, 0, len(arr))
	for _, rawPrice := range arr {

		xlmPrices = append(xlmPrices, xlmPrice{timestamp: int64(rawPrice[0]), price: rawPrice[1]})
	}
	return
}

func getXLMPrices() (xlmPrices []xlmPrice, err error) {

	resp, err := http.Get("https://api.stellar.expert/explorer/public/xlm-price")
	if err != nil {
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return
	}
	xlmPrices, err = unmarshalXLMPricesJSON(body)
	return
}

type historyItem struct {
	Timestamp    int64     `json:"ts"`
	TradedAmount int64     `json:"traded_amount"`
	Price        []float64 `json:"price"`
}

func getTFTPriceHistory() (history []historyItem, err error) {
	resp, err := http.Get("https://api.stellar.expert/explorer/public/asset/TFT-GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47/stats-history")
	if err != nil {
		return
	}
	defer resp.Body.Close()
	history = []historyItem{}
	err = json.NewDecoder(resp.Body).Decode(&history)
	return
}

// GetMontlyPrice calculates a MontlyPrice using stellar.expert
func GetMontlyPrice(month time.Month, year int) (m MonthlyPrice, err error) {
	m.Month = month
	m.Year = year
	xlmPrices, err := getXLMPrices()
	if err != nil {
		return
	}
	fmt.Println("Last XLM Price: timestamp:", xlmPrices[0].timestamp, "price:", xlmPrices[0].price)
	tftPriceHistory, err := getTFTPriceHistory()
	if err != nil {
		return
	}
	l := tftPriceHistory[len(tftPriceHistory)-1]
	fmt.Println("Last tft history item: timestamp:", l.Timestamp, "traded amount:", l.TradedAmount, "price:", l.Price)

	startTimestamp := time.Date(year, month, 1, 0, 0, 0, 0, time.UTC).Unix()

	nextmonth := (month + 1) % 12
	endyear := year
	if nextmonth != month+1 {
		endyear += 1
	}
	endTimestamp := time.Date(endyear, nextmonth, 1, 0, 0, 0, 0, time.UTC).Unix()

	weighted_average_price := 0.0
	total_volume := 0.0
	for _, historypoint := range tftPriceHistory {
		if historypoint.Timestamp < startTimestamp || historypoint.Timestamp > endTimestamp {
			continue
		}

	}
	if total_volume > 0.0 {
		weighted_average_price /= total_volume
	}
	m.Price = weighted_average_price
	return
}
