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
    // public ClassLoader loader;
    public static final String CLASSNAME = "com.test.App";
    public static final String METHODNAME = "yell";
    public static final String TESTTP = "System.out.println(\"Ha!\");";
    // public static final String CLASSNAME = "travel.service.TravelServiceImpl";
    // public static final String METHODNAME = "query";
    // public static final String TESTTP=  "io.opentelemetry.api.trace.Span.current().addEvent(\"[LUMOS] Event attached inside query() \"" + 
                    //   "+ endPlaceName + \" -- without Tracer!!!!!!\")";
        
    public static final int TESTLINE = 10;

    public AgentThread(Instrumentation inst){
        this.inst = inst;
        this.agent = new JVMAgent(inst);
        this.manager = new DynamicManager(this.agent);
        // this.agent.loader = loader;
    }

    // public static void getLoader(ClassLoader loader){
    //     AgentThread.loader = loader;
    // }

    public void connect(String controllerAddr){
        try {
            this.client = new WebSocketClient(new URI(controllerAddr), this);
            client.send("LUMOS-AGENT");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void handleMessage(String message){
        System.out.println("Handling " + message);
    }

    @Override
    public void run(){

        // Wait Until we hooked the Spring classloader
        while(LumosAgent.cloader == null) ;


        // Connect to websocket controller server
        connect("ws://localhost:8001");

        // A test of adding a tracepoint, then remove it...
        int seconds = 90;
        for(int i = 0; i < seconds; i++){
            try{
                Thread.sleep(1000);
            }
            catch(Exception e){
            }
            System.out.println("[LUMOS] Count " + (seconds - i));
        }
        System.out.println("[LUMOS] Instrumenting...");


        DynamicModification modifyMethod = new InstructionModification(CLASSNAME, METHODNAME, TESTTP, TESTLINE);
        
        try{
            this.manager.add(modifyMethod);
            this.manager.install();
            System.out.println("[LUMOS] Instrumented!");
            this.client.close();
        }
        catch(Exception e){
            e.printStackTrace();
        }
        
        
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
        
        while(true){

        }
    }
}