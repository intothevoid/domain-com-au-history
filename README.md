# domain-com-au-history
A telegram bot which accepts a property address in Australia and returns a screenshot of the property history (if available)

### @propertyhelperbot
https://t.me/propertyhelperbot/

## Screenshot
<img src="https://raw.githubusercontent.com/intothevoid/domain-com-au-history/main/sshot.jpeg" width="50%" height="50%"></img>

## Usage / Demo
Simply send the bot a property address in Australia and it will return a screenshot of the property history (if available)

Demo is available at - https://t.me/propertyhelperbot/

## How to use and deploy your own custom property helper bot
1. Clone the repo
2. Update config.env with the following variables:
    - telegram_token: Your telegram bot token
    - chrome_path: Path to your chrome binary (if using docker leave unchanged)
3. Run `docker build -t property-helper .`
4. Run `sudo docker run --name property-helper --restart unless-stopped -d --env-file config.env property-helper`
5. Open telegram and search for your bot
