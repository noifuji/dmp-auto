package spreadsheetapis;
import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.client.util.store.FileDataStoreFactory;
import com.google.api.services.sheets.v4.Sheets;
import com.google.api.services.sheets.v4.SheetsScopes;
import com.google.api.services.sheets.v4.model.ValueRange;
import com.google.api.services.sheets.v4.model.AppendValuesResponse;
import com.google.api.services.sheets.v4.model.BatchGetValuesResponse;
import com.google.api.services.drive.DriveScopes;
import com.google.api.client.http.HttpRequestInitializer;
import com.google.api.client.http.HttpRequest;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.security.GeneralSecurityException;
import java.util.Collections;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;
import java.util.Arrays;


public class SpreadSheetApis {
  private static final JsonFactory JSON_FACTORY = JacksonFactory.getDefaultInstance();
  private static final String TOKENS_DIRECTORY_PATH = "data";
  private static final List<String> SCOPES = Arrays.asList(SheetsScopes.SPREADSHEETS,DriveScopes.DRIVE);
	
	
  private Sheets service;
	
  public SpreadSheetApis(String appname, String strClientSecrets) throws IOException, GeneralSecurityException{
    System.out.println("Start SpreadSheetApis");
    final NetHttpTransport HTTP_TRANSPORT = GoogleNetHttpTransport.newTrustedTransport();
    System.out.println("Start to create a sheet service instance");
    this.service = new Sheets.Builder(HTTP_TRANSPORT, JSON_FACTORY, getCredentials(HTTP_TRANSPORT, strClientSecrets))
                 .setApplicationName(appname)
                 .build();
    System.out.println("End SpreadSheetApis");
  }
	
  private HttpRequestInitializer setHttpTimeout(final HttpRequestInitializer requestInitializer) {
    return new HttpRequestInitializer() {
      @Override
      public void initialize(HttpRequest httpRequest) throws IOException {
        requestInitializer.initialize(httpRequest);
        httpRequest.setConnectTimeout(1 * 60000);  // 1 minute connect timeout
        httpRequest.setReadTimeout(1 * 60000);     // 1 minute read timeout
      }
    };
  }
	
  private static Credential getCredentials(final NetHttpTransport HTTP_TRANSPORT, String strClientSecrets) throws IOException {
    System.out.println("Start getCredentials");
    GoogleClientSecrets clientSecrets = GoogleClientSecrets.load(JSON_FACTORY, new java.io.StringReader(strClientSecrets));
    System.out.println("GoogleClientSecrets.load");

    // Build flow and trigger user authorization request.
    GoogleAuthorizationCodeFlow flow = new GoogleAuthorizationCodeFlow.Builder(HTTP_TRANSPORT, JSON_FACTORY, clientSecrets, SCOPES)
                                     .setDataStoreFactory(new FileDataStoreFactory(new java.io.File(TOKENS_DIRECTORY_PATH)))
                                     .setAccessType("offline")
                                     .build();
    System.out.println("new GoogleAuthorizationCodeFlow.Builder");
    LocalServerReceiver receiver = new LocalServerReceiver.Builder().setPort(8888).build();
    System.out.println("End getCredentials");
    return new AuthorizationCodeInstalledApp(flow, receiver).authorize("user");
  }

  public List<List<Object>> read(String spreadsheetId, String range, String dimension) throws IOException  {
    if (!dimension.equals("ROWS") && !dimension.equals("COLUMNS")) {
      throw new IOException();
    }
    Sheets.Spreadsheets.Values.Get request = service.spreadsheets().values()
                                           .get(spreadsheetId, range);
    request.setMajorDimension(dimension);
                        
    ValueRange response = request.execute();
    List<List<Object>> values = response.getValues();
    return values;
  }
	
  public List<List<List<Object>>> batchRead(String spreadsheetId, List<String> ranges, String dimension) {
  	
    List<List<List<Object>>> result = new ArrayList<List<List<Object>>>();
  	
    if (!dimension.equals("ROWS") && !dimension.equals("COLUMNS")) {
      return result;
    }
  	
  	try{
        Sheets.Spreadsheets.Values.BatchGet request = service.spreadsheets().values()
                                                    .batchGet(spreadsheetId);
        request.setRanges(ranges);
        request.setMajorDimension(dimension);
                            
        BatchGetValuesResponse response = request.execute();
        List<ValueRange> valueRanges = response.getValueRanges();
      	
        Iterator<ValueRange> iterator = valueRanges.iterator();
        while(iterator.hasNext()) {
          result.add(iterator.next().getValues());
        }
  	}catch(Exception e){
  			return result;
  		}
    return result;
  }
	
  public void write(String spreadsheetId, String range, List<List<Object>> values, String dimension) throws IOException {
    if (!dimension.equals("ROWS") && !dimension.equals("COLUMNS")) {
      throw new IOException();
    }
    System.out.println("write is called");
    String valueInputOption = "USER_ENTERED";
    ValueRange requestBody = new ValueRange();
    requestBody.setValues(values);
    requestBody.setMajorDimension(dimension);

    Sheets.Spreadsheets.Values.Update request =
    service.spreadsheets().values().update(spreadsheetId, range, requestBody);
    request.setValueInputOption(valueInputOption);

    request.execute();
    System.out.println("request was executed");
  }
	
  public void append(String spreadsheetId, String range, List<List<Object>> values, String dimension) throws IOException {
    if (!dimension.equals("ROWS") && !dimension.equals("COLUMNS")) {
      throw new IOException();
    }
    String valueInputOption = "USER_ENTERED";
    ValueRange requestBody = new ValueRange();
    requestBody.setValues(values);
    requestBody.setMajorDimension(dimension);

    AppendValuesResponse result = service.spreadsheets().values().append(spreadsheetId, range, requestBody)
                                .setValueInputOption(valueInputOption)
                                .execute();
		
    System.out.printf("%d cells appended.\n", result.getUpdates().getUpdatedCells());
  }

}
