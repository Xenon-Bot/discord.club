use std::task::{Context, Poll};
use actix_service::{Service, Transform};
use actix_web::dev::{ServiceRequest, ServiceResponse};
use actix_web::{Error, HttpResponse, web};
use futures::future::{ok, Either, Ready};

use crate::AppState;

pub struct CheckAuth;

impl<S, B> Transform<S> for CheckAuth
    where
        S: Service<Request=ServiceRequest, Response=ServiceResponse<B>, Error=Error>,
        S::Future: 'static
{
    type Request = ServiceRequest;
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Transform = CheckAuthMiddleware<S>;
    type InitError = ();
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ok(CheckAuthMiddleware { service })
    }
}

pub struct CheckAuthMiddleware<S> {
    service: S,
}

impl<S, B> Service for CheckAuthMiddleware<S>
    where
        S: Service<Request=ServiceRequest, Response=ServiceResponse<B>, Error=Error>,
        S::Future: 'static,
{
    type Request = ServiceRequest;
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Future = Either<S::Future, Ready<Result<Self::Response, Self::Error>>>;

    fn poll_ready(&mut self, cx: &mut Context) -> Poll<Result<(), Self::Error>> {
        self.service.poll_ready(cx)
    }

    fn call(&mut self, req: ServiceRequest) -> Self::Future {
        if let Some(state) = req.app_data::<web::Data<AppState>>() {
            if let Some(token) = req.headers().get("Authorization") {
                // let db = state.db.clone();
                // JWT validation and add user to app data?
                Either::Left(self.service.call(req))
            } else {
                Either::Right(ok(req.into_response(
                    HttpResponse::Unauthorized()
                        .finish()
                        .into_body(),
                )))
            }
        } else {
            Either::Right(ok(req.into_response(
                HttpResponse::InternalServerError()
                    .body("Can't retrieve app state")
                    .into_body(),
            )))
        }
    }
}

