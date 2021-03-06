#!/bin/bash

#
# constants
#
phoenicis_dir=~/.Phoenicis/
shortcuts_dir="$$phoenicis_dir/shortcuts/"

name="${APP_NAME}"
shortcut="$$shortcuts_dir/${APP_NAME_CLEAN}.shortcut"
install_id="${SCRIPT_INSTALL_ID}"

# check if app has been installed already
if [ ! -f "$$shortcut" ]; then
    # do not use Wine runtime (e.g. Notepad++ crashes otherwise)
    # TODO: use graphical installer instead of CLI
    /app/jre/bin/java -Dapplication.repository.list=/app/phoenicis/repositories.json -Dapplication.environment.wineRuntime=false --add-modules=jdk.crypto.ec,java.base,javafx.base,javafx.web,javafx.media,javafx.graphics,javafx.controls,java.naming,java.sql,java.scripting,jdk.internal.vm.ci,jdk.internal.vm.compiler,org.graalvm.truffle,jdk.jsobject,jdk.xml.dom --module-path /app/phoenicis/lib/ -XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -cp "/app/phoenicis/lib/*" --upgrade-module-path=/app/phoenicis/lib/compiler.jar org.phoenicis.cli.PhoenicisCLI -install $$install_id
fi

# do not use Wine runtime (e.g. Notepad++ crashes otherwise)
# TODO: use phoenicis-shortcut-runner.sh
/app/jre/bin/java -Dapplication.repository.list=/app/phoenicis/repositories.json -Dapplication.environment.wineRuntime=false --add-modules=jdk.crypto.ec,java.base,javafx.base,javafx.web,javafx.media,javafx.graphics,javafx.controls,java.naming,java.sql,java.scripting,jdk.internal.vm.ci,jdk.internal.vm.compiler,org.graalvm.truffle,jdk.jsobject,jdk.xml.dom --module-path /app/phoenicis/lib/ -XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -cp "/app/phoenicis/lib/*" --upgrade-module-path=/app/phoenicis/lib/compiler.jar org.phoenicis.cli.PhoenicisCLI -run "$$name"
