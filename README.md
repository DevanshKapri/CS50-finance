# Finalysis
A web app via which we can manage portfolios of stocks. This tool allows us to check real stocks’ actual prices and portfolios’ values, it will also let you buy (okay, “buy”) and sell (okay, “sell”) stocks by querying IEX for stocks’ prices.

## Configuring
Before getting started on this assignment, we’ll need to register for an API key in order to be able to query IEX’s data. To do so, follow these steps:

- Visit iexcloud.io/cloud-login#/register/.
- Select the “Individual” account type, then enter your email address and a password, and click “Create account”.
- Once registered, scroll down to “Get started for free” and click “Select Start” to choose the free plan.
- Once you’ve confirmed your account via a confirmation email, visit https://iexcloud.io/console/tokens.
- Copy the key that appears under the Token column (it should begin with pk_).
- In a terminal window within CS50 IDE, execute:
`$ export API_KEY=value`
where value is that (pasted) value, without any space immediately before or after the =. You also may wish to paste that value in a text document somewhere, in case you need it again later.
