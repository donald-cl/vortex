package com.sbf.memoryjar;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.content.Intent;
import android.content.Context;
import android.util.Log;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;

public class LoginActivity extends Activity {

    private EditText  username=null;
    private EditText  password=null;
    private TextView attempts;
    private Button login;
    private int counter = 5;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        username = (EditText)findViewById(R.id.usernameField);
        password = (EditText)findViewById(R.id.passwordField);
        attempts = (TextView)findViewById(R.id.numAttempts);
        attempts.setText(Integer.toString(counter));
        login = (Button)findViewById(R.id.loginButton);
    }

    public void login(View view){

       //TODO: FIX THE LOGIN LOGIC - RIGHT NOW ONLY ADMIN/ADMIN AUTHENTICATES
        if(username.getText().toString().equals("admin") &&
                password.getText().toString().equals("admin")){
            Toast.makeText(getApplicationContext(), "Redirecting...",
                    Toast.LENGTH_SHORT).show();

            Toast.makeText(getBaseContext(), "Please wait, connecting to server.", Toast.LENGTH_SHORT).show();

            Thread verifyCredentials = new Thread(new Runnable() {
                private final HttpClient Client = new DefaultHttpClient();
                private String URL = "http://androidexample.com/media/webservice/getPage.php";

                private final Handler handler = new Handler() {
                    public void handleMessage(Message msg) {

                        String aResponse = msg.getData().getString("message");

                        if (aResponse.equals("Server Data Android Example")) {
                            //Toast.makeText(
                            //        getBaseContext(),
                            //        "Server Response: "+aResponse,
                            //        Toast.LENGTH_LONG).show();


                            Intent intent = new Intent(LoginActivity.this, HomeActivity.class);
                            startActivity(intent);
                        }
                        else
                        {
                            // ALERT MESSAGE
                            Toast.makeText(
                                    getBaseContext(),
                                    "Not Got Response From Server- "+aResponse,
                                    Toast.LENGTH_LONG).show();
                        }

                    }

                };

                private void threadMsg(String msg) {

                    if (!msg.equals(null) && !msg.equals("")) {
                        Message msgObj = handler.obtainMessage();
                        Bundle b = new Bundle();
                        b.putString("message", msg);
                        msgObj.setData(b);
                        handler.sendMessage(msgObj);
                    }
                }

                public void run() {
                    try {
                        String SetServerString = "";
                        HttpGet httpget = new HttpGet(URL);
                        ResponseHandler<String> responseHandler = new BasicResponseHandler();
                        SetServerString = Client.execute(httpget, responseHandler);
                        threadMsg(SetServerString);
                    } catch (Throwable t) {
                        // just end the background thread
                        Log.i("Animation", "Thread  exception " + t);
                    }
                }

            });

            verifyCredentials.start();
        }
        else{
            Toast.makeText(getApplicationContext(), "Wrong Credentials",
                    Toast.LENGTH_SHORT).show();
            attempts.setBackgroundColor(Color.RED);
            counter--;
            attempts.setText(Integer.toString(counter));
            if(counter==0){
                login.setEnabled(false);
            }

        }

    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_login, menu);
        return true;
    }

}