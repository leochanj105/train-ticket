import os
collector_addr = "c220g1-030623.wisc.cloudlab.us"
for fdir in os.listdir('./'):
    if("ts-" in fdir and "service" in fdir):
        lines = []
        with open(fdir+"/Dockerfile", "r") as f:
            # print(fdir)
            has_otlp = False
            has_lumos = False
            need_jars = False
            for line in f:
                if "ADD" in line and "opentelemetry" in line:
                    has_otlp = True
                if "ADD" in line and "LumosAgent" in line:
                    has_lumos = True
                if "-Xmx200m" in line:
                    need_jars = True
            f.seek(0)
            for line in f:
                if "CMD" in line and need_jars:
                    if not has_otlp:
                        lines.append("ADD ./opentelemetry-javaagent.jar /app/\n")
                    if not has_lumos:
                        lines.append("ADD ./LumosAgent-jar-with-dependencies.jar /app/\n")
                if('-Xmx200m' in line):
                    idx = line.index('"java", ') + len('"java", ')
                    str = ""
                    if "LumosAgent" not in line:
                        str += '"-javaagent:/app/LumosAgent-jar-with-dependencies.jar", "-Dsname=' +fdir +'", '
                    if "opentelemetry-javaagent" not in line:
                        str += '"-javaagent:/app/opentelemetry-javaagent.jar", "-Dotel.service.name='
                        str += fdir +'", "-Dotel.exporter.otlp.endpoint=http://' + collector_addr + ':4317", ' 
                    lines.append(line[:idx] + str + line[idx:])
                else:
                    lines.append(line)
            # print(lines)
        with open(fdir +"/Dockerfile", "w") as f:
        #with open("test1", "w") as f:
            for line in lines:
                f.write(line)
