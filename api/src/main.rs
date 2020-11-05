use std::io;

use actix_web::{middleware, web, App, HttpServer};
use mongodb;
use std::env;

mod endpoints;
mod auth;

#[derive(Clone)]
pub struct AppState {
    pub db: mongodb::Database,
    pub redirect_uri: String,
    pub client_id: String,
    pub client_secret: String
}

#[actix_web::main]
async fn main() -> io::Result<()> {
    let mut db_options = mongodb::options::ClientOptions::parse("mongodb://localhost:27017")
        .await
        .expect("Invalid mongodb url");
    db_options.app_name = Some("Discord.Club".to_string());
    let db_client = mongodb::Client::with_options(db_options).unwrap();
    let db = db_client.database("dclub");

    let redirect_uri = env::var("REDIRECT_URI").expect("No REDIRECT_URI given");
    let client_secret = env::var("CLIENT_SECRET").expect("No CLIENT_SECRET given");
    let client_id = env::var("CLIENT_ID").expect("No CLIENT_ID given");

    let state = web::Data::new(AppState {
        db,
        redirect_uri,
        client_secret,
        client_id
    });

    let host = env::var("HOST").expect("No HOST given");

    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .wrap(middleware::Logger::default())
            .wrap(auth::CheckAuth)
            .data(web::JsonConfig::default().limit(4096))
            .service(endpoints::oauth::exchange_tokens)
            .service(endpoints::embeds::create_template)
    })
        .bind(host)?
        .run()
        .await
}
