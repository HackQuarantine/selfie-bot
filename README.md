# Selfie Scraper Discord Bot

Discord bot to get selfies from the `#selfies` channel and save them locally!

# Development

To run the script:

```
make
```

This will automatically install all the dependencies. Make sure you have a
`creds.json` filled in!

You might have to increase ImageMagicks limits by editing `/etc/ImageMagic-6/policy.xml`. Ran into this issue on a standard ubuntu install. See this [issue](https://github.com/ImageMagick/ImageMagick/issues/396)

To clean the environment

```
make clean
```
