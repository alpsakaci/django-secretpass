import environ


env = environ.Env()
# reading .env file
environ.Env.read_env()

SP_PASSPHRASE = env("SP_PASSPHRASE")
