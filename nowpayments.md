API Documentation
Instant Payments Notifications

IPN (Instant payment notifications, or callbacks) are used to notify you when transaction status is changed.
To use them, you should complete the following steps:

    Generate and save the IPN Secret key in Payment Settings tab at the Dashboard;

    Insert your URL address where you want to get callbacks in create_payment request. The parameter name is ipn_callback_url. You will receive payment updates (statuses) to this URL address.**
    Please, take note that we cannot send callbacks to your localhost unless it has dedicated IP address.**

    important Please make sure that firewall software on your server (i.e. Cloudflare) does allow our requests to come through. It may be required to whitelist our IP addresses on your side to get it. The list of these IP addresses can be requested at partners@nowpayments.io;

    You will receive all the parameters at the URL address you specified in (2) by POST request;
    The POST request will contain the x-nowpayments-sig parameter in the header.
    The body of the request is similiar to a get payment status response body.
    You can see examples in "Webhook examples" section.

    Sort the POST request by keys and convert it to string using
    JSON.stringify (params, Object.keys(params).sort()) or the same function;

    Sign a string with an IPN-secret key with HMAC and sha-512 key;

    Compare the signed string from the previous step with the x-nowpayments-sig , which is stored in the header of the callback request;
    If these strings are similar, it is a success.
    Otherwise, contact us on support@nowpayments.io to solve the problem.

Example of creating a signed string at Node.JS
Plain Text

function sortObject(obj) {
  return Object.keys(obj).sort().reduce(
    (result, key) => {
      result[key] = (obj[key] && typeof obj[key] === 'object') ? sortObject(obj[key]) : obj[key]
      return result
    },
    {}
  )
}
const hmac = crypto.createHmac('sha512', notificationsKey);
hmac.update(JSON.stringify(sortObject(params)));
const signature = hmac.digest('hex');

Example of comparing signed strings in PHP
Plain Text

function tksort(&$array)
  {
  ksort($array);
  foreach(array_keys($array) as $k)
    {
    if(gettype($array[$k])=="array")
      {
      tksort($array[$k]);
      }
    }
  }
function check_ipn_request_is_valid()
    {
        $error_msg = "Unknown error";
        $auth_ok = false;
        $request_data = null;
        if (isset($_SERVER['HTTP_X_NOWPAYMENTS_SIG']) && !empty($_SERVER['HTTP_X_NOWPAYMENTS_SIG'])) {
            $recived_hmac = $_SERVER['HTTP_X_NOWPAYMENTS_SIG'];
            $request_json = file_get_contents('php://input');
            $request_data = json_decode($request_json, true);
            tksort($request_data);
            $sorted_request_json = json_encode($request_data, JSON_UNESCAPED_SLASHES);
            if ($request_json !== false && !empty($request_json)) {
                $hmac = hash_hmac("sha512", $sorted_request_json, trim($this->ipn_secret));
                if ($hmac == $recived_hmac) {
                    $auth_ok = true;
                } else {
                    $error_msg = 'HMAC signature does not match';
                }
            } else {
                $error_msg = 'Error reading POST data';
            }
        } else {
            $error_msg = 'No HMAC signature sent.';
        }
    }

Example comparing signed signatures in Python
python

import json 
import hmac 
import hashlib
def np_signature_check(np_secret_key, np_x_signature, message):
    sorted_msg = json.dumps(message, separators=(',', ':'), sort_keys=True)
    digest = hmac.new(
    str(np_secret_key).encode(), 
    f'{sorted_msg}'.encode(),
    hashlib.sha512)
    signature = digest.hexdigest()
    if signature == np_x_signature:
        return
    else:
        print("HMAC signature does not match")

Usually you will get a notification per each step of processing payments, withdrawals, or transfers, related to custodial recurring payments.

The webhook is being sent automatically once the transaction status is changed.

You also can request an additional IPN notification using your NOWPayments dashboard.

Please note that you should set up an endpoint which can receive POST requests from our server.

Before going production we strongly recommend to make a test request to this endpoint to ensure it works properly.



POSTCreate invoice
https://api.nowpayments.io/v1/invoice

Creates a payment link. With this method, the customer is required to follow the generated url to complete the payment. Data must be sent as a JSON-object payload.

Request fields:

    price_amount (required) - the amount that users have to pay for the order stated in fiat currency. In case you do not indicate the price in crypto, our system will automatically convert this fiat amount into its crypto equivalent. NOTE: Some of the assets (KISHU, NWC, FTT, CHR, XYM, SRK, KLV, SUPER, OM, XCUR, NOW, SHIB, SAND, MATIC, CTSI, MANA, FRONT, FTM, DAO, LGCY), have a maximum price limit of ~$2000;
    price_currency (required) - the fiat currency in which the price_amount is specified (usd, eur, etc);
    pay_currency (optional) - the specified crypto currency (btc, eth, etc), or one of available fiat currencies if it's enabled for your account (USD, EUR, ILS, GBP, AUD, RON);
    If not specified, can be chosen on the invoice_url
    ipn_callback_url (optional) - url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io";
    order_id (optional) - internal store order ID, e.g. "RGDBP-21314";
    order_description (optional) - internal store order description, e.g. "Apple Macbook Pro 2019 x 1";
    success_url(optional) - url where the customer will be redirected after successful payment;
    cancel_url(optional) - url where the customer will be redirected after failed payment;
    is_fixed_rate(optional) - boolean, can be true or false. Required for fixed-rate exchanges;
    NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired";
    is_fee_paid_by_user(optional) - boolean, can be true or false. Required for fixed-rate exchanges with all fees paid by users;
    NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired";

SUCCESSFUL RESPONSE FIELDS
Name	Type	Description
id	String	Invoice ID
token_id	String	Internal identifier
order_id	String	Order ID specified in request
order_description	String	Order description specified in request
price_amount	String	Base price in fiat
price_currency	String	Ticker of base fiat currency
pay_currency	String	Currency your customer will pay with. If it's 'null' your customer can choose currency in web interface.
ipn_callback_url	String	Link to your endpoint for IPN notifications catching
invoice_url	String	Link to the payment page that you can share with your customer
success_url	String	Customer will be redirected to this link once the payment is finished
cancel_url	String	Customer will be redirected to this link if the payment fails
partially_paid_url	String	Customer will be redirected to this link if the payment gets partially paid status
payout_currency	String	Ticker of payout currency
created_at	String	Time of invoice creation
updated_at	String	Time of latest invoice information update
is_fixed_rate	Boolean	This parameter is 'True' if Fixed Rate option is enabled and 'false' if it's disabled
is_fee_paid_by_user	Boolean	This parameter is 'True' if Fee Paid By User option is enabled and 'false' if it's disabled
HEADERS
x-api-key

{{api-key}}

(Required) Your NOWPayments API key
Content-Type

application/json

(Required) Your payload has to be JSON object
Bodyraw (json)

example:
{
  "price_amount": 1000,
  "price_currency": "usd",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "ipn_callback_url": "https://nowpayments.io",
  "success_url": "https://nowpayments.io",
  "cancel_url": "https://nowpayments.io",
  "partially_paid_url": "https://nowpayments.io",
  "is_fixed_rate": true,
  "is_fee_paid_by_user": false
}

Example Request
curl --location 'https://api.nowpayments.io/v1/invoice' \
--header 'x-api-key: {{api-key}}' \
--header 'Content-Type: application/json' \
--data '{
  "price_amount": 1000,
  "price_currency": "usd",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "ipn_callback_url": "https://nowpayments.io",
  "success_url": "https://nowpayments.io",
  "cancel_url": "https://nowpayments.io"
}



Example Response

{
  "id": "4522625843",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "price_amount": "1000",
  "price_currency": "usd",
  "pay_currency": null,
  "ipn_callback_url": "https://nowpayments.io",
  "invoice_url": "https://nowpayments.io/payment/?iid=4522625843",
  "success_url": "https://nowpayments.io",
  "cancel_url": "https://nowpayments.io",
  "created_at": "2020-12-22T15:05:58.290Z",
  "updated_at": "2020-12-22T15:05:58.290Z"
}
