for i in ` find . -maxdepth 1  -name "ts-*" ` ; do cp opentelemetry-javaagent.jar $i/ ; done
