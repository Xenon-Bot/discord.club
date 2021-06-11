use std::{env, error::Error};
use tokio::stream::StreamExt;
use twilight_gateway::{
    cluster::{Cluster, ShardScheme},
    queue::{LargeBotQueue, Queue},
    Event,
};
use twilight_model::gateway::{Intents, payload::MessageCreate};
use twilight_http::Client as HttpClient;
use std::sync::Arc;
use tracing_subscriber;
use std::fs::File;
use std::io::Read;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error + Send + Sync>> {
    tracing_subscriber::fmt::init();

    let token = env::var("DISCORD_TOKEN")
        .expect("No discord token given");
    let intents = Intents::from_bits(4608)
        .expect("Invalid intent value given");

    let http = HttpClient::new(&token);
    let gateway = http
        .gateway()
        .authed()
        .await
        .expect("Can't fetch gateway info");

    let queue: Arc<Box<dyn Queue>> = Arc::new(
        Box::new(
            LargeBotQueue::new(
                gateway
                    .session_start_limit
                    .max_concurrency as usize,
                &http,
            ).await
        )
    );
    println!("{:?}", gateway);

    let scheme = ShardScheme::Range {
        from: 0,
        to: gateway.shards - 1,
        total: gateway.shards,
    };
    let cluster = Cluster::builder(&token, intents)
        .shard_scheme(scheme)
        .queue(queue)
        .http_client(http.clone())
        .build()
        .await?;

    let cluster_spawn = cluster.clone();
    tokio::spawn(async move {
        cluster_spawn.up().await;
    });

    let mut events = cluster.events();
    while let Some((_shard_id, event)) = events.next().await {
        match event {
            Event::MessageCreate(msg) => {
                if msg.content.starts_with(">") {
                    tokio::spawn(handle_command(http.clone(), msg));
                } else if msg.content.starts_with("/") {
                    tokio::spawn(handle_slash_message(http.clone(), msg));
                }
            }
            _ => {}
        }
    }

    Ok(())
}

async fn handle_slash_message(http: HttpClient, msg: Box<MessageCreate>) -> Result<(), Box<dyn Error + Send + Sync>> {
    let commands = [
        "/format", "/webhook", "/json", "/edit", "/embed"
    ];

    for cmd in &commands {
        if msg.content.starts_with(cmd) {
            let mut f = File::open("troubleshooting.png").expect("troubleshooting file missing");
            let mut buffer = Vec::new();
            f.read_to_end(&mut buffer)?;


            http.create_message(msg.channel_id)
                .content(
                    "Seems like you tried to use Embed Generator with **Slash Commands** ✌️ \
                    \n\nIf the commands don't show up for you try to **invite Embed Generator again** using \
                    the following link: <https://discord.club/invite> \
                    \nAlso make sure you have the following **setting enabled** for them to show up.\
                    \n\nIf you continue to have problems, \
                    consider asking for help on our discord server: <https://discord.club/discord>"
                )?
                .attachment("troubleshooting.png", buffer)
                .await?;
            break;
        }
    }

    Ok(())
}

async fn handle_command(http: HttpClient, msg: Box<MessageCreate>) -> Result<(), Box<dyn Error + Send + Sync>> {
    let mut chars = msg.content.chars();
    chars.next();
    let cmd = chars.as_str();

    let mut args = Vec::new();
    for arg in cmd.split(" ") {
        args.push(arg.to_string())
    }

    if args.len() == 0 {
        return Ok(());
    }

    let cmd = match args[0].as_str() {
        "invite" => Some(String::from("invite")),
        "ping" => Some(String::from("ping")),
        "support" => Some(String::from("support")),
        "embed" => Some(String::from("embed")),
        "edit" =>  Some(String::from("edit")),
        "json" => Some(String::from("json")),
        "webhook" => Some(String::from("webhook")),
        "format" => Some(String::from("format")),
        "help" => Some(String::from("help")),
        _ => None
    };

    if let Some(cmd_name) = cmd {
        http.create_message(msg.channel_id)
            .content(format!("\
            Hey, Embed Generator is now using Slash Commands! 🎉 \
            \n\n**Please use the following command instead**:\
            \n```/{}```
            \nIf you continue to have problems, consider asking for help on \
            our discord server: <https://discord.club/discord>", cmd_name))?
            .await?;
    }

    Ok(())
}
