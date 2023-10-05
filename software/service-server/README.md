# SkyLink Smart Server

Server for running smart cam.

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 10.1.6.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).


#### Build:

        docker build -f docker/Dockerfile -t cmb87/skylink-nodeserver:latest .
        docker build -f docker/Dockerfile_arm32v7 -t cmb87/skylink-nodeserver:arm32v7-latest .

#### Run:
        docker run -p 5000:5000 cmb87/skylink-nodeserver:latest
        
#### Push:

        docker push cmb87/skylink-nodeserver:latest
        
#### Pull:

        docker pull cmb87/skylink-nodeserver:latest
        
Author: cmb87