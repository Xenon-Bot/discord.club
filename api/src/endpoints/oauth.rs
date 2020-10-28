use actix_web::{HttpResponse, Responder, post, web, client::Client};
use serde::{Deserialize, Serialize};
use mongodb::bson;
use serde_json::json;

use crate::AppState;

#[derive(Serialize, Deserialize)]
pub struct ExchangePayload {
    pub code: String
}

#[derive(Serialize, Deserialize)]
pub struct TokenPayload {
    pub access_token: String
}

#[derive(Serialize, Deserialize)]
pub struct UserData {
    pub id: String,
    pub username: String,
}

#[post("/oauth/exchange")]
pub async fn exchange_tokens(state: web::Data<AppState>, payload: web::Json<ExchangePayload>) -> impl Responder {
    let db = state.db.clone();

    let exchange_payload = json!({
        "client_id": state.client_id,
        "client_secret": state.client_secret,
        "redirect_uri": state.redirect_uri,
        "grant_type": "authorization_code",
        "code": payload.0.code,
        "scope": "identify",
    });

    let client = Client::new();

    let res = client
        .post("https://discord.com/api/oauth2/token")
        .send_json(&exchange_payload)
        .await;

    let token_data = match res {
        Ok(mut resp) => {
            if resp.status().is_success() {
                match resp.json::<TokenPayload>().await {
                    Ok(token_data) => token_data,
                    Err(err) => return HttpResponse::BadRequest().body(format!("{:#?}", err))
                }
            } else {
                return HttpResponse::BadRequest().finish();
            }
        }
        Err(err) => return HttpResponse::InternalServerError().body(format!("{:#?}", err))
    };

    let res = client
        .get("https://discord.com/api/users/@me")
        .send()
        .await;

    let user_data = match res {
        Ok(mut resp) => {
            if resp.status().is_success() {
                match resp.json::<UserData>().await {
                    Ok(user_data) => user_data,
                    Err(err) => return HttpResponse::BadRequest().body(format!("{:#?}", err))
                }
            } else {
                return HttpResponse::BadRequest().finish();
            }
        }
        Err(err) => return HttpResponse::InternalServerError().body(format!("{:#?}", err))
    };

    match db.collection("users").insert_one(bson::doc! {
        "_id": user_data.id,
        "name": user_data.username
    }, None).await {
        Ok(db_result) => {
            HttpResponse::Created().json(db_result.inserted_id)
        }
        Err(_err) => {
            return HttpResponse::InternalServerError().finish();
        }
    }
}