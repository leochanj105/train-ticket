package com.agent;

import java.net.URI;
import javax.websocket.ClientEndpoint;
import javax.websocket.CloseReason;
import javax.websocket.ContainerProvider;
import javax.websocket.OnClose;
import javax.websocket.OnMessage;
import javax.websocket.OnOpen;
import javax.websocket.Session;
import javax.websocket.WebSocketContainer;

import java.io.IOException;
@ClientEndpoint
public class WebSocketClient {
    public Session session;
    private MessageHandler handler;

    public WebSocketClient(URI uri, MessageHandler handler){
        try {
            this.handler = handler;
            WebSocketContainer container = ContainerProvider.getWebSocketContainer();
            System.out.println("connecting...");
            container.connectToServer(this, uri);
            System.out.println("connected");
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @OnOpen
    public void onOpen(Session session){
        this.session = session;
    }

    @OnClose
    public void onClose(Session session, CloseReason reason){

    }

    @OnMessage
    public void onMessage(String msg){
        this.handler.handleMessage(msg);
    }

    // @OnMessage
    // public void onMessage(ByteBuffer bytes) {
    //         System.out.println(bytes);
    // }

    public void send(String message) {
        this.session.getAsyncRemote().sendText(message);
    }

    public void close() throws IOException{
        this.session.close();
    }
}