package com.example.projectcypher;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ActionBar;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    Button button;
    EditText editname;
    EditText editpass;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getSupportActionBar().hide();

        editname = findViewById(R.id.editTextText);
        editpass = findViewById(R.id.editTextPass);
        button = findViewById(R.id.loginbutton);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(editname.getText().toString().equals("Kronos") && editpass.getText().toString().equals("alohomora")){
                    Intent intent = new Intent(MainActivity.this, MenuScreen.class);
                    startActivity(intent);
                }
                else{
                    Toast.makeText(getApplicationContext(),"Incorrect LoginId or Password", Toast.LENGTH_LONG).show();
                }
            }
        });
    }

}