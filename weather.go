package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/go-resty/resty/v2"
)

const (
	apiKey  = "50c72145cfa7e37fbead5e2700d4fe41"
	baseURL = "http://api.openweathermap.org/data/2.5/weather"
)

type WeatherResponse struct {
	Main struct {
		Temp     float64 `json:"temp"`
		Humidity int     `json:"humidity"`
	} `json:"main"`
	Wind struct {
		Speed float64 `json:"speed"`
	} `json:"wind"`
	Weather []struct {
		Description string `json:"description"`
	} `json:"weather"`
	Name string `json:"name"`
}

func getWeather(city string) (string, error) {
	client := resty.New()
	url := fmt.Sprintf("%s?q=%s&appid=%s&units=metric", baseURL, city, apiKey)

	resp, err := client.R().
		SetResult(&WeatherResponse{}).
		Get(url)
	if err != nil {
		return "", err
	}

	if resp.StatusCode() != http.StatusOK {
		if resp.StatusCode() == http.StatusNotFound {
			return "", fmt.Errorf("error 404")
		}
		return "", fmt.Errorf("error: %s for city %s", resp.Status(), city)
	}

	weather := resp.Result().(*WeatherResponse)
	jsonData, err := json.Marshal(weather)
	if err != nil {
		return "", err
	}

	return string(jsonData), nil
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Please specify a city as an argument")
	}

	city := os.Args[1]
	weather, err := getWeather(city)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(weather)
}
