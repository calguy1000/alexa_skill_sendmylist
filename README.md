# alexa_sendmylist
A simple alexa skill written in python that will send the user's current shopping list to their registered email address.

This skill uses docker to contain the development environment, and configuration tools, and docker-compose for convenience.

I wrote this skill purely as an exercise in using chatgpt and other AI tools to give me a start on development, to re-familiarize myself with Python, and to have a skill I would find useful for my home automation setup.


### Prerequisites
- docker
- docker compose
- gnu make
- An AWS account

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/calguy1000/alexa_sendmylist.git
    cd alexa_sendmylist
    ```
1. Setup amazon SES
    Ensure you have amazon SES configured properly to send emails under your domain

1. Modify the environment variables in the docker-compose.yml
    Environment variables:
    - AWS_PROFILE=default # Use AWS Credentials from your AS environment
    - FROM_EMAIL # Replace with your verified email address
    - AWS_REGION # replace with your AWS SES Region

1. Build the container
    ```sh
    make build
    ```
1. Configure the ASK command line client
    Open a shell in the container
    ```sh
    make shell
    ```
    Inside the container, configure ask
    ```sh
    worker@7572844d5ba3:~$ ask configure --no-browser
    ```
    A URL will be printed on the screen.  Copy and paste it into your browser. Login using your amazon developer account.  Copy the authorization token and secret key that are displayed into the terminal When asked.

1. Create a new alexa skill
   While still in the container's terminal
    ```sh
    worker@7572844d5ba3:~$ ask init
    ```
    TODO

1.  Deploy the skill
    From within the container's terminal
    ```sh
    worker@7572844d5ba3:~$ ask deploy
    ```
    or from outside of the container's terminal
    ```sh
    make deploy
    ```

## Contributing

We welcome contributions! Please see the CONTRIBUTING.md file for guidelines on how to contribute.

## License

This project is licensed under the terms of the [LICENSE](http://_vscodecontentref_/3) file.

## Security Disclosures

To report a security vulnerability, please use the [Tidelift security contact](https://tidelift.com/security). Tidelift will coordinate the fix and disclosure with maintainers.

## Maintainers

- [@sethmlarson](https://github.com/sethmlarson) (Seth M. Larson)
- [@pquentin](https://github.com/pquentin) (Quentin Pradet)
- [@illia-v](https://github.com/illia-v) (Illia Volochii)
- [@theacodes](https://github.com/theacodes) (Thea Flowers)
- [@haikuginger](https://github.com/haikuginger) (Jess Shapiro)
- [@lukasa](https://github.com/lukasa) (Cory Benfield)
- [@sigmavirus24](https://github.com/sigmavirus24) (Ian Stapleton Cordasco)