# labor-notifier

This is a [Twilio](https://www.twilio.com/) application that utilizes [Flask](http://flask.pocoo.org/), [PostgreSQL](https://www.postgresql.org/), and [Heroku](https://www.heroku.com/). It serves a unique purpose, but is written in a way that anyone can deploy it if they want to use it.

I wrote this out of a lack of desire to call or text everyone who may want to know when my wife has our baby.

* Users texts the specified Twilio number and register their phone numbers with the application.
* Then, when my wife (or whoever), has the baby, I (or the owner) can text a secret phrase to the number.
  * Upon receiving this text, the application will go through each of the registered numbers and notify them baby has been born.
* When a user texts the Twilio number, they are automatically signed up and can removed themselves by texting REMOVE (case insensitive).
* If your secret phrase is `secret`, then to begin the notification process you would text the number "`secret` Your message goes here".
* Once the secret phrase has been received, any future texts to this number will automatically reply with this response as the baby has already been born. You can leave it up as long as you want after that.

## Configuration

### Twilio

Create a free account with [Twilio](https://www.twilio.com/) and buy a number with SMS capabilities. On your new Twilio dashboard, copy the phone number, account sid, and auth token, we'll use them later when configuring the Heroku application.

Open the sidebar (the three dots `...`) and navigate to **Phone Numbers** under **Super Network**. Select your number and scroll down to the **Messaging** area. We'll replace the Webhook URL with the application we establish with Heroku next.


### Heroku

Create a free account with [Heroku](http://www.heroku.com)

If you're not familiar with Heroku, I'll avoid command line instructions and have you use their website. In which case you'll need to fork this repository (**Fork** button at the top of this GitHub page). Otherwise, you can simply clone it and deploy this code to your Heroku app via the command line interface.

* Sign up for a free [Heroku account](https://signup.heroku.com/dc)
* From your Dashboard, [Create a new app](https://dashboard.heroku.com/new-app). Name it something unique!
* You'll be navigatged to the **Deploy** page. In the **Deployment method** section, select the GitHub option and type `labor-notifier` into the *repo-name* input, click the Search button, and click the **Connect** button for the repository
* Select the **Overview** tab and in the **Installed add-ons** section select the **Configure Add-ons** link. In the **Add-ons** section search for **Heroku Postgres** and select the **Hobby Dev &mdash; Free** Plan and click **Provision**

Next, navigate to **Settings** and click the **Reveal Config Vars** button in the Config Vars section to add the following keys and their appropriate values from the previous setup steps with Discord and Reddit. You should have an existing variable named `DATABASE_URL` from provisioning the **Heroku Postgres** instance. In the input boxes below, enter the following values:

`BABY_NICKNAME` &mdash; how you want the application to refer to your baby, example: `Baby Johnson` or `Peanut`, etc.

`BORN_PHRASE` &mdash; this is your secret phrase to trigger the alert to all persons who have signed up to be notified. Make it something unqiue and memorable

`SID` &mdash; this is the value from your Twilio dashboard we copied earlier

`TOKEN` &mdash; this is the value from your Twilio dashboard we copied earlier

`URL` &mdash; with heroku, the URL will always be your application's name as the subdomain, as an example if you named your app `babynotifier` your url should be `https://babynotifier.herokuapp.com/`.

**All of these values need to be set for the application to work.**

There are two **Optional** values you can set:

`TWILIO_VOICE` &mdash; the default is `female` but your other options are `male` and `alice`. [You can read more about Twilio's voices here](https://www.twilio.com/docs/voice/twiml/say#voice).

`PORT` &mdash; the default is `8080` but you can change as you see fit

Finally, back to your [Twilio Phone Numbers](https://www.twilio.com/console/phone-numbers/incoming) dashboard, we need to update your **Messaging** webhook URL to point to your endpoint, again with the example of `babynotifier` being your Heroku app name, the URL should be `https://babynotifier.herokuapp.com/api/sms`

## Use

1. Finally, on your [Heroku dashboard](https://dashboard.heroku.com/apps) select your application and navigate to **Resources**. Ensure your **Free Dynos** is enabled, and it should show it's configured with `web python run.py`.
2. Next, hand out the Twilio number to those who you wish to have notified about the baby and have them text it to enroll.
3. Finally, once it comes time, send your `BORN_PHRASE` in a text to the Twilio number and the application will handle notifying everyone who registered.
4. Make sure once you have the baby you stop running your instance of the application. Until you do so anyone who texts it will continue to receive the message you sent with the `BORN_PHRASE`.
