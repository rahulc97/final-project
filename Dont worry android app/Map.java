package com.example.dontworryrealtimeupdater;


import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;
import com.mapbox.mapboxsdk.Mapbox;
import com.mapbox.mapboxsdk.annotations.Marker;
import com.mapbox.mapboxsdk.annotations.MarkerOptions;
import com.mapbox.mapboxsdk.geometry.LatLng;
import com.mapbox.mapboxsdk.maps.MapView;
import com.mapbox.mapboxsdk.maps.MapboxMap;
import com.mapbox.mapboxsdk.maps.OnMapReadyCallback;
import com.mapbox.mapboxsdk.maps.Style;
import static com.mapbox.mapboxsdk.Mapbox.getApplicationContext;
import java.io.IOException;
import java.util.List;
import java.util.Locale;


public class Map extends Fragment {
    private MapView mapView;
    private FirebaseFirestore db = FirebaseFirestore.getInstance();
    private static final String KEY_LATITUDE="latitude";
    private static final String KEY_LONGITUDE="longitude";
    private double latitude;
    private double longitude;
    Marker marker = null;
    private DocumentReference docRef = db.collection("location").document("current_location");


    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {

        View view=inflater.inflate(R.layout.activity_map,container,false);

        mapView = (MapView) view.findViewById(R.id.mapView);
        mapView.onCreate(savedInstanceState);
        mapView.getMapAsync(new OnMapReadyCallback() {
            @Override
            public void onMapReady(@NonNull final MapboxMap mapboxMap) {

                mapboxMap.setStyle(Style.MAPBOX_STREETS, new Style.OnStyleLoaded() {
                    @Override
                    public void onStyleLoaded(@NonNull Style style) {
//real time update
                        docRef.addSnapshotListener(new EventListener<DocumentSnapshot>() {
                            @Override
                            public void onEvent(@Nullable DocumentSnapshot snapshot,
                                                @Nullable FirebaseFirestoreException e) {
                                if (e != null) {
                                    Log.w("message", "Listen failed.", e);
                                    return;
                                }
                                if (snapshot != null && snapshot.exists()) {
                                    latitude= (double) snapshot.get(KEY_LATITUDE);
                                    longitude=(double) snapshot.get(KEY_LONGITUDE);
                                    Toast.makeText(getActivity(), "Longitude : "+longitude+" Latitude : "+latitude, Toast.LENGTH_LONG).show();
                                    Geocoder geocoder;
                                    List<Address> addresses;
                                    geocoder = new Geocoder(getActivity(), Locale.getDefault());
                                    Location location=new Location("");
                                    location.setLatitude(latitude);
                                    location.setLongitude(longitude);
                                    String address = "",city= "",state= "",country="",postalcode="",knownname="";

                                    try {

                                        addresses = geocoder.getFromLocation(location.getLatitude(), location.getLongitude(), 1);
                                        address = addresses.get(0).getAddressLine(0); // If any additional address line present than only, check with max available address lines by getMaxAddressLineIndex()
                                        city = addresses.get(0).getLocality();
                                        state = addresses.get(0).getAdminArea();
                                        country = addresses.get(0).getCountryName();
                                        postalcode = addresses.get(0).getPostalCode();
                                        knownname = addresses.get(0).getFeatureName();
                                        if(marker!=null)
                                        {
                                            marker.remove();}
                                        marker = mapboxMap.addMarker(new MarkerOptions()
                                                .position(new LatLng(latitude, longitude))
                                                .title(address));
                                        Toast.makeText(getActivity(),address+city+country,Toast.LENGTH_SHORT).show();
                                    } catch (IOException e1) {
                                        e1.printStackTrace();
                                    }

                                    Log.d("message", "Current data: " + snapshot.getData());
                                } else {
                                    Log.d("message", "Current data: null");
                                }
                            }
                        });

                    }
                });

            }
        });


        return  view;
    }


    public void onStart() {
        super.onStart();
        mapView.onStart();
    }

    @Override
    public void onResume() {
        super.onResume();
        mapView.onResume();
    }

    @Override
    public void onPause() {
        super.onPause();
        mapView.onPause();
    }

    @Override
    public void onStop() {
        super.onStop();
        mapView.onStop();
    }

    @Override
    public void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        mapView.onSaveInstanceState(outState);
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        mapView.onLowMemory();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        mapView.onDestroy();
    }

}
