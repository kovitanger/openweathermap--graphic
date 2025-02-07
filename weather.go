package main

import (
	"fmt"
	"log"

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

func main() {
	cities := []string{
		"Tokyo",
		"Chongqing",
		"Delhi",
		"Shanghai",
		"Dhaka",
		"Sao Paulo",
		"Mexico City",
		"Cairo",
		"Beijing",
		"Mumbai",
	}

	client := resty.New()

	for _, city := range cities {
		url := fmt.Sprintf("%s?q=%s&appid=%s&units=metric", baseURL, city, apiKey)

		resp, err := client.R().
			SetResult(&WeatherResponse{}).
			Get(url)

		if err != nil {
			log.Printf("Ошибка при выполнении запроса для города %s: %v", city, err)
			continue
		}

		if resp.StatusCode() != 200 {
			log.Printf("Ошибка: %s для города %s", resp.Status(), city)
			continue
		}

		weather := resp.Result().(*WeatherResponse)
		fmt.Printf("Погода в городе %s:\n", weather.Name)
		fmt.Printf("Температура: %.1f°C\n", weather.Main.Temp)
		fmt.Printf("Влажность: %d%%\n", weather.Main.Humidity)
		fmt.Printf("Скорость ветра: %.1f м/с\n", weather.Wind.Speed)
		fmt.Printf("Описание: %s\n", weather.Weather[0].Description)
		fmt.Println("------------------------------")
	}
}
