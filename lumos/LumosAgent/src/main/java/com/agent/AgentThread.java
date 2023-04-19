package com.agent;
import java.lang.instrument.Instrumentation;
import java.lang.Thread;
import javassist.CannotCompileException;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtConstructor;
import javassist.NotFoundException;
import java.lang.instrument.UnmodifiableClassException;
import java.util.Collection;

import java.lang.reflect.Field;
import java.lang.ClassLoader;
import java.util.Vector;
import java.net.URI;

import com.google.common.collect.Lists;
// import edu.brown.cs.systems.dynamicinstrumentation.JVMAgent;
import edu.brown.cs.systems.dynamicinstrumentation.*;

import javassist.bytecode.AnnotationsAttribute;
import javassist.bytecode.annotation.Annotation;
import javassist.bytecode.ConstPool;

public class AgentThread implements Runnable, MessageHandler{
    public Instrumentation inst;
    public JVMAgent agent;
    public DynamicManager manager;
    public WebSocketClient client;
    public String sname = System.getProperty("sname");
    // public ClassLoader loader;
    //public static final String CLASSNAME = "com.test.App";
    //public static final String METHODNAME = "yell";
    //public static final String TESTTP = "System.out.println(\"Ha!\");";
    public static final String WITHSPAN = "io.opentelemetry.instrumentation.annotations.WithSpan";
    public static final String CLASSNAME = "travel.service.TravelServiceImpl";
    public static final String METHODNAME = "query";
    public static final String TESTTP=  "io.opentelemetry.api.trace.Span.current().addEvent(\"[LUMOS] HELLO!!!!!!!!\");";
        
    public static final int TESTLINE = 158;

    public AgentThread(Instrumentation inst){
        this.inst = inst;
        this.agent = new JVMAgent(inst);
        this.manager = new DynamicManager(this.agent);
	System.out.println("SNAME=" + sname);
        // this.agent.loader = loader;
    }

    // public static void getLoader(ClassLoader loader){
    //     AgentThread.loader = loader;
    // }

    public void connect(String controllerAddr){
        try {
            this.client = new WebSocketClient(new URI(controllerAddr), this);
            client.send(sname);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void handleMessage(String message){
        System.out.println("Handling " + message);
	if(message.equals("keepalive"))
	    return;

        String[] traceArgs = message.split(",", 0);
	System.out.println(traceArgs);
	String classname = traceArgs[0];
	String methodname = traceArgs[1];
	String code = traceArgs[2];
	int ln = Integer.parseInt(traceArgs[3]);
	//DynamicModification mod = new AnnotationModification(classname, methodname, WITHSPAN);
	DynamicModification mod = new InstructionModification(classname, methodname, code, ln);
	try{
	    this.manager.add(mod);
            this.manager.install();
	}
	catch(Exception e){
            e.printStackTrace();
	}
	System.out.println("Instrumented!");
    }

    @Override
    public void run(){
        // Wait Until we hooked the Spring classloader
        while(LumosAgent.cloader == null) ;


        // Connect to websocket controller server
        connect("ws://lumos:8765");
	
	
        // A test of adding a tracepoint, then remove it...
/*        int seconds = 20;
        for(int i = 0; i < seconds; i++){
            try{
                Thread.sleep(1000);
            }
            catch(Exception e){
            	e.printStackTrace();
            }
            System.out.println("[LUMOS] Count " + (seconds - i));
        }
        System.out.println("[LUMOS] Instrumenting...");


        DynamicModification modifyMethod = new InstructionModification(CLASSNAME, METHODNAME, TESTTP, TESTLINE);
        
        try{
            this.manager.add(modifyMethod);
            this.manager.install();
            System.out.println("[LUMOS] Instrumented!");
            //this.client.close();
        }
        catch(Exception e){
            e.printStackTrace();
        }
  */     
/**        
        seconds = 60;
        for(int i = 0; i < seconds; i++){
            try{
                Thread.sleep(1000);
            }
            catch(Exception e){
            }
            System.out.println("[LUMOS] Count " + (seconds - i));
        }

        System.out.println("[LUMOS] Uninstrumenting...");
        try{
            this.manager.remove(modifyMethod);
            this.manager.install();
            System.out.println("[LUMOS] Uninstrumented!");

            
        }
        catch(Exception e){
            e.printStackTrace();
        }
**/        
        while(true){

        }
    }
}
