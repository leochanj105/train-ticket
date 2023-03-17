import os
for fdir in os.listdir('./'):
    if("ts-" in fdir and "service" in fdir):
        lines = []
        with open(fdir+"/Dockerfile", "r") as f:
            # print(fdir)
            for line in f:
                if("ADD" in line and "/app/" in line):
                    lines.append("ADD ./opentelemetry-javaagent.jar /app/\n")
                if('-Xmx200m' in line):
                    idx = line.index('"-Xmx200m') 
                    str = '"-javaagent:/app/opentelemetry-javaagent.jar", "-Dotel.service.name=' + fdir +'", "-Dotel.exporter.otlp.endpoint=http://collector:4317", '
                    lines.append(line[:idx] + str + line[idx:])
                else:
                    lines.append(line)
            # print(lines)
        with open(fdir +"/Dockerfile", "w") as f:
        #with open("test1", "w") as f:
            for line in lines:
                f.write(line)
