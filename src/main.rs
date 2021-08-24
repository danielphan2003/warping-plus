
use chrono::{self, SecondsFormat};
use const_format::{concatcp, formatcp};
use fake::{Fake, StringFaker};
use reqwest::{ 
    Client,
    header::{
        ACCEPT_ENCODING,
        CONNECTION,
        CONTENT_TYPE,
        HOST,
        USER_AGENT,
        HeaderMap
    },
};
use serde_derive::{Serialize, Deserialize};
use std::path::Path;
use tokio::fs;
use toml;

const DIGITS: &str = "0123456789";

const ASCII_LETTERS: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

const ALPHANUMERIC: &str = concatcp!(ASCII_LETTERS, DIGITS);

const CONFIG_FILE_NAME: &str = "warping-plus.toml";

const DEFAULT_CONFIG_PATH: &str = formatcp!("~/.config/warping-plus/{CONFIG_FILE_NAME}");

macro_rules! FORMAT_BASE_URL { () => { "https://api.cloudflareclient.com/v0a{}/reg" }; }

macro_rules! FORMAT_FCM_TOKEN { () => { "{}:APA91b{}" }; }

#[derive(Debug, Deserialize)]
struct Config {
    referrer: String,
    parallel_requests: u8,
    proxies_file: String,
}

#[derive(Debug, Serialize)]
struct WarpClientInfo {
    fcm_token: String,
    install_id: String,
    locale: String,
    key: String,
    referrer: String,
    tos: String,
    r#type: String,
    warp_enabled: bool,
}

fn gen_digit_string(len: usize) -> String {
    StringFaker::with(
        DIGITS.to_string().into_bytes(),
        len,
    ).fake::<String>()
}

fn gen_alphanumeric_string(len: usize) -> String {
    StringFaker::with(
        ALPHANUMERIC.to_string().into_bytes(),
        len,
    ).fake::<String>()
}

async fn open_config_file() -> Result<Config, Box<dyn std::error::Error>> {
    let config_path = if Path::new(CONFIG_FILE_NAME).exists() {
        Ok(CONFIG_FILE_NAME)
    } else {
        if Path::new(DEFAULT_CONFIG_PATH).exists() {
            Ok(DEFAULT_CONFIG_PATH)
        } else {
            Err("No config file found! Define one in warping-plus.toml")
        }
    };
    
    let raw_config_str = fs::read_to_string(config_path.unwrap()).await?;
    Ok(toml::from_str(&raw_config_str).unwrap())
}

async fn open_proxies_file(proxies_file: String) -> Result<String, String> {
    if Path::new(&proxies_file).exists() {
        Ok(fs::read_to_string(proxies_file).await?)
    } else {
        Err("Unknown path to proxies file!".to_string())
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = open_config_file().await;

    let client = Client::new();

    let mut headers = HeaderMap::new();
    headers.insert(CONTENT_TYPE, "application/json; charset=UTF-8".parse().unwrap());
    headers.insert(HOST, "api.cloudflareclient.com".parse().unwrap());
    headers.insert(CONNECTION, "Keep-Alive".parse().unwrap());
    headers.insert(ACCEPT_ENCODING, "gzip".parse().unwrap());
    headers.insert(USER_AGENT, "okhttp/3.12.1".parse().unwrap());

    let fcm_token_id = gen_alphanumeric_string(134);

    let install_id = gen_alphanumeric_string(22);

    let client_info = WarpClientInfo {
        fcm_token: format!(FORMAT_FCM_TOKEN!(), install_id.clone(), fcm_token_id),
        install_id,
        locale: "es_ES".to_string(),
        key: format!("{}=", gen_alphanumeric_string(43)),
        referrer: "53ad0ed7-ddf1-493c-a9dc-5ae81cc1541a".to_string(),
        tos: chrono::Utc::now().to_rfc3339_opts(SecondsFormat::Millis, false),
        warp_enabled: false,
        r#type: "Android".to_string(),
    };

    let client_id = gen_digit_string(3);
    let base_url = format!(FORMAT_BASE_URL!(), client_id);
    let res = client.post(base_url)
        .headers(headers)
        .json(&client_info)
        .send()
        .await?;

    Ok(())
}
