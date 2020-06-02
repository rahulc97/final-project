package com.example.dontworryrealtimeupdater;

import androidx.annotation.Nullable;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.fragment.app.Fragment;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.material.navigation.NavigationView;
import com.google.firebase.Timestamp;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;


public class Updater extends  Fragment implements View.OnClickListener {

    private FirebaseFirestore db = FirebaseFirestore.getInstance();
    private static final String KEY_MESSAGE="message";
    private static final String KEY_TIME="time";
    private static final String KEY_TIME_24="time24";
    EditText editmessage ;
    Button btn;
    String rpi_time="00:00:00";
    String time_24="00:00:01";
    private DocumentReference docRef = db.collection("messages").document("rpi");
    private DocumentReference docRef2 = db.collection("messages").document("android");
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container,@Nullable Bundle savedInstanceState) {

            View view=inflater.inflate(R.layout.activity_updater,container,false);
            btn=(Button) view.findViewById(R.id.btn) ;
            btn.setOnClickListener(this);
            return  view;
    }
    @Override
    public void onStart() {
        super.onStart();
//        setContentView(R.layout.activity_updater);

        editmessage = (EditText) getView().findViewById(R.id.editmessage);
        final TextView textmessage = (TextView) getView().findViewById(R.id.textmessage);
        final TextView textmessage1 = (TextView) getView().findViewById(R.id.textmess1);
        final TextView textmessage3 = (TextView) getView().findViewById(R.id.textmess3);
        final TextView timemessage1 = (TextView) getView().findViewById(R.id.time_msg_1);
        final TextView timemessage2 = (TextView) getView().findViewById(R.id.time_msg_2);
        final TextView timemessage3 = (TextView) getView().findViewById(R.id.time_msg_3);
        final TextView texttime = (TextView) getView().findViewById(R.id.texttime);

        docRef.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot snapshot,
                                @Nullable FirebaseFirestoreException e) {
                if (e != null) {
                    Log.w("message", "Listen failed.", e);
                    return;
                }

                if (snapshot != null && snapshot.exists()) {

                    String message=" "  ;
                    String time=" ";
                    rpi_time= (String) snapshot.get(KEY_TIME_24);
                    message = (String) snapshot.get(KEY_MESSAGE);
                    time=  (String) snapshot.get(KEY_TIME);
                    textmessage.setText(message);
                    timemessage2.setText(time);
                }
            }
        });

        docRef2.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot snapshot,
                                @Nullable FirebaseFirestoreException e) {
                if (e != null) {
                    Log.w("message", "Listen failed.", e);
                    return;
                }

                if (snapshot != null && snapshot.exists()) {

                    String message=" "  ;
                    String time=" ";
                    message = (String) snapshot.get(KEY_MESSAGE);
                    time=  (String) snapshot.get(KEY_TIME);
                    time_24=  (String) snapshot.get(KEY_TIME_24);
                    if(rpi_time!=null && time_24!=null) {
                        int cmp = rpi_time.compareTo(time_24);
                        if (cmp >= 0) {
                            textmessage1.setVisibility(View.VISIBLE);
                            timemessage1.setVisibility(View.VISIBLE);
                            textmessage1.setText(message);
                            timemessage1.setText(time);
                            textmessage3.setVisibility(View.INVISIBLE);
                            timemessage3.setVisibility(View.INVISIBLE);

                        } else {
                            textmessage3.setVisibility(View.VISIBLE);
                            timemessage3.setVisibility(View.VISIBLE);
                            textmessage3.setText(message);
                            timemessage3.setText(time);
                            textmessage1.setVisibility(View.INVISIBLE);
                            timemessage1.setVisibility(View.INVISIBLE);
                        }
                    }else{
                        textmessage3.setVisibility(View.VISIBLE);
                        textmessage3.setText(message);
                        textmessage1.setVisibility(View.INVISIBLE);
                    }
                }
            }
        });

    }
        @Override
        public void onClick(View view) {
            //OnCLick Stuff
            String typedMessage=" ";
            typedMessage= String.valueOf(editmessage.getText());
            String currentTime_24 = new SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(new Date());
            String currentTime = new SimpleDateFormat("hh:mm a", Locale.getDefault()).format(new Date());
            Map<String, Object> data = new HashMap<>();
            data.put(KEY_MESSAGE, typedMessage);
            data.put(KEY_TIME,currentTime);
            data.put(KEY_TIME_24,currentTime_24);
            docRef2.set(data);
            editmessage.setText(null);
            Toast.makeText(getActivity(), "Message : send " , Toast.LENGTH_SHORT).show();
        }


}