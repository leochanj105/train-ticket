cd lumos/LumosAgent && mvn assembly:assembly && cd ../..
for i in ` find . -maxdepth 1  -name "ts-*" ` ; do cp opentelemetry-javaagent.jar $i/ ; done
for i in ` find . -maxdepth 1  -name "ts-*" ` ; do cp lumos/LumosAgent/target/LumosAgent-jar-with-dependencies.jar $i/ ; done

