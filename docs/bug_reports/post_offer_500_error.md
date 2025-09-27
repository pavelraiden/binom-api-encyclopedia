Subject: [Bug Report/Documentation Request] 500 Internal Server Error when creating an offer via POST /offer endpoint

Dear Binom Development Team,

I hope this message finds you well. I am writing to report an issue we have encountered while trying to create an offer using the Binom API and to request your assistance in resolving it.

**Summary:**

We are consistently receiving a 500 Internal Server Error when attempting to create an offer via the `POST /offer` endpoint, despite trying various request body variations. This is blocking our work on creating comprehensive workflows for our "Binom API Encyclopedia".

**Steps to Reproduce:**

1. Send a POST request to `https://pierdun.com/public/api/v1/offer`
2. Include the `api-key` header with a valid API key
3. Set the `Content-Type` header to `application/json`
4. Include the following JSON payload in the request body:
   ```json
   {
       "offer": {
           "name": "Final Test Offer with Status",
           "url": "http://final-test.com",
           "affiliate_network_id": 1,
           "payout": 3.0,
           "status": "active"
       }
   }
   ```

**Expected Result:**

A 200 OK or 201 Created status code, along with the created offer details in the response body.

**Actual Result:**

A 500 Internal Server Error with the following JSON response:
```json
{"errors":{"title":"TypeError","detail":"strtoupper(): Argument #1 ($string) must be of type string, null given","message":"strtoupper(): Argument #1 ($string) must be of type string, null given","code":0,"status":500}}
```

**Analysis:**

The `strtoupper(): Argument #1 ($string) must be of type string, null given` error clearly indicates that the backend expects a mandatory string field that we are not sending, causing the error. This field is not present in the official Swagger documentation or, consequently, in our encyclopedia.

**Request:**

Could you please either fix the bug (if it is indeed a bug) or, more likely, provide the complete and accurate documentation for the `POST /offer` endpoint, including all mandatory fields and their types? A working example request would also be greatly appreciated.

We would be immensely grateful if you could help us unblock our work by providing the necessary information or resolving the issue. If you need any further details or have any questions, please don't hesitate to ask.

Thank you in advance for your time and assistance.

Best regards,

[Your Name]

