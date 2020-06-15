# phoenicis-flatpak-${APP_FLATPAK_ID}
Phoenicis app flatpak for ${APP_NAME}

### Build
from current directory:
```
git clone https://github.com/PhoenicisOrg/phoenicis.git
cd phoenicis
mvn package -DskipTests
cd ..
cp phoenicis/phoenicis-dist/target/phoenicis-flatpak.zip .
flatpak-builder build-dir org.phoenicis.${APP_FLATPAK_ID}.yml --force-clean --user --install
```

### Run
```
flatpak run org.phoenicis.${APP_FLATPAK_ID}
```

### How it works
- If the app is not installed (i.e. normally for the first run), perform an installation with Phoenicis. This also installs the required Wine version.
- Otherwise run the app.
