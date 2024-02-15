package config

import (
	"strings"

	"github.com/spf13/viper"
	"github.com/zaigie/palworld-server-tool/internal/logger"
	"github.com/zaigie/palworld-server-tool/internal/system"
)

type Config struct {
	Web struct {
		Port             int      `mapstructure:"port"`
		Password         string   `mapstructure:"password"`
		Tls              bool     `mapstructure:"tls"`
		CertPath         string   `mapstructure:"cert_path"`
		KeyPath          string   `mapstructure:"key_path"`
		TrustedProxies   []string `mapstructure:"trusted_proxies"`
		BroadcastAddress string   `mapstructure:"broadcast_address"`
	}
	Rcon struct {
		Address      string `mapstructure:"address"`
		Password     string `mapstructure:"password"`
		Timeout      int    `mapstructure:"timeout"`
		SyncInterval int    `mapstructure:"sync_interval"`
	} `mapstructure:"rcon"`
	Save struct {
		Path         string `mapstructure:"path"`
		DecodePath   string `mapstructure:"decode_path"`
		SyncInterval int    `mapstructure:"sync_interval"`
	} `mapstructure:"save"`
	Manage struct {
		KickNonWhitelist bool `mapstructure:"kick_non_whitelist"`
	}
}

func Init(cfgFile string, conf *Config) {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
		viper.SetConfigType("yaml")
	} else {
		viper.AddConfigPath(".")
		viper.SetConfigName("config")
		viper.SetConfigType("yaml")
	}

	err := viper.ReadInConfig()
	if err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			logger.Warn("config file not found, try to read from env\n")
		} else {
			logger.Panic("config file was found but another error was produced\n")
		}
	}

	viper.SetDefault("web.port", 8080)
	viper.SetDefault("web.trusted_proxies", []string{})
	localIp, err := system.GetLocalIP()
	if err != nil {
		logger.Error(err)
	}
	viper.SetDefault("web.broadcast_address", localIp)
	viper.SetDefault("rcon.timeout", 5)
	viper.SetDefault("rcon.sync_interval", 60)
	viper.SetDefault("save.sync_interval", 600)

	viper.SetEnvPrefix("")
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "__"))
	viper.AutomaticEnv()

	err = viper.Unmarshal(conf)
	if err != nil {
		logger.Panicf("Unable to decode config into struct, %s", err)
	}
}
