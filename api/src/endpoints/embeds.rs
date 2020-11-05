use actix_web::{HttpResponse, Responder, post, web, client::Client};
use serde::{Deserialize, Serialize};
use mongodb::bson;

use crate::AppState;

#[derive(Serialize, Deserialize)]
pub struct CreateTemplatePayload {
    pub name: String
}

#[post("/embeds/templates")]
pub async fn create_template(state: web::Data<AppState>, payload: web::Json<CreateTemplatePayload>) -> impl Responder {
    let db = state.db.clone();

    match db.collection("embeds.templates").insert_one(bson::doc! {
        "name": payload.0.name
    }, None).await {
        Ok(db_result) => {
            HttpResponse::Created().json(db_result.inserted_id)
        }
        Err(_err) => {
            return HttpResponse::InternalServerError().finish();
        }
    }
}