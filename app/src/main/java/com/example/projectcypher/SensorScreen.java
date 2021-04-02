package com.example.projectcypher;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Objects;
import java.util.concurrent.TimeUnit;

public class SensorScreen extends AppCompatActivity{

    private SensorManager msensorManager;
    private Sensor gyrosensor;
    private SensorEventListener gyroscopeEventListener;
    private String val;
    TextView textView;
    Button connectbutton;
    Button disconnectbutton;
    private HandlerThread mSensorThread;
    private Handler mSensorHandler;
    private boolean connection = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sensor_screen);
        Objects.requireNonNull(getSupportActionBar()).hide();
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        textView = (TextView) findViewById(R.id.SensorData);
        connectbutton = (Button) findViewById(R.id.connectionbutton);
        disconnectbutton = (Button) findViewById(R.id.terminationbutton);
        msensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        gyrosensor = msensorManager != null ? msensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE) : null;
        if(gyrosensor==null){
            Toast.makeText(getApplicationContext(), "Nah bro. That didn't work", Toast.LENGTH_SHORT);
        }
        gyroscopeEventListener = new SensorEventListener() {
            @Override
            public void onSensorChanged(SensorEvent event) {
                val = (Math.round(event.values[0])) + "," +
                        (Math.round(event.values[1])) + "," + (Math.round(event.values[2]));
                /*
                first value: move to face mobile upward: +ve values, downwards: -ve values
                second value: move to face mobile towards left: +ve values, rightwards: -ve values
                third values: rotate mobile anticlockwise: +ve, clockwise: -ve values
                */
                Log.d("val output", val);
            }

            @Override
            public void onAccuracyChanged(Sensor sensor, int accuracy) {}
        };

        disconnectbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                connection = false;
            }
        });

        connectbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                connection = true;
                try {
                    Socket s = new Socket("192.168.1.30", 5000);
                    DataOutputStream outputStream = new DataOutputStream(s.getOutputStream());
                    while(connection){
                        outputStream.writeUTF(val);
                        TimeUnit.SECONDS.sleep(1);
                    }
                    outputStream.flush();
                    outputStream.close();
                    DataInputStream inputStream = new DataInputStream(s.getInputStream());
                    String string = (String)inputStream.readUTF();
                    Toast.makeText(getApplicationContext(), string, Toast.LENGTH_LONG).show();
                    s.close();

                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
    }
    @Override
    protected void onStart() {
        super.onStart();
        mSensorThread = new HandlerThread("Sensor Thread", Thread.MAX_PRIORITY);
        mSensorThread.start();
        mSensorHandler = new Handler(mSensorThread.getLooper());
        msensorManager.registerListener(gyroscopeEventListener,
                gyrosensor,
                SensorManager.SENSOR_DELAY_FASTEST,
                mSensorHandler);
    }
    @Override
    protected void onStop(){
        super.onStop();
        msensorManager.unregisterListener(gyroscopeEventListener);
        mSensorThread.quitSafely();
    }
}