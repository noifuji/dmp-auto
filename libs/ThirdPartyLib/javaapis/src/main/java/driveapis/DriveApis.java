package driveapis;
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
import com.google.api.services.drive.Drive;
import com.google.api.services.drive.DriveScopes;
import com.google.api.services.drive.model.File;
import com.google.api.services.drive.model.FileList;
import com.google.api.services.sheets.v4.SheetsScopes;
import com.google.api.client.http.FileContent;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.security.GeneralSecurityException;
import java.util.Collections;
import java.util.List;
import java.util.Arrays;

public class DriveApis {
  private static final JsonFactory JSON_FACTORY = JacksonFactory.getDefaultInstance();
  private static final String TOKENS_DIRECTORY_PATH = "data";
  private static final List<String> SCOPES = Arrays.asList(DriveScopes.DRIVE,SheetsScopes.SPREADSHEETS);
	
  private Drive service;
	
  public DriveApis(String appname, String strClientSecrets) throws IOException, GeneralSecurityException{
    final NetHttpTransport HTTP_TRANSPORT = GoogleNetHttpTransport.newTrustedTransport();
    this.service = new Drive.Builder(HTTP_TRANSPORT, JSON_FACTORY, getCredentials(HTTP_TRANSPORT, strClientSecrets))
                 .setApplicationName(appname)
                 .build();
  }

  private static Credential getCredentials(final NetHttpTransport HTTP_TRANSPORT, String strClientSecrets) throws IOException {
    GoogleClientSecrets clientSecrets = GoogleClientSecrets.load(JSON_FACTORY, new java.io.StringReader(strClientSecrets));

    // Build flow and trigger user authorization request.
    GoogleAuthorizationCodeFlow flow = new GoogleAuthorizationCodeFlow.Builder(HTTP_TRANSPORT, JSON_FACTORY, clientSecrets, SCOPES)
                                     .setDataStoreFactory(new FileDataStoreFactory(new java.io.File(TOKENS_DIRECTORY_PATH)))
                                     .setAccessType("offline")
                                     .build();
    LocalServerReceiver receiver = new LocalServerReceiver.Builder().setPort(8888).build();
    return new AuthorizationCodeInstalledApp(flow, receiver).authorize("user");
  }
	
  public String uploadFile(String filename, String path, String parentFolderId) throws IOException {
    File fileMetadata = new File();
    fileMetadata.setName(filename);
    fileMetadata.setParents(Collections.singletonList(parentFolderId));
    java.io.File filePath = new java.io.File(path);
    FileContent mediaContent = new FileContent("image/png", filePath);
    File file = service.files().create(fileMetadata, mediaContent)
              .setFields("id")
              .execute();
  	return file.getId();
  }
	
  public String createFolder(String foldername, String parentFolderId) throws IOException {
    File fileMetadata = new File();
    fileMetadata.setName(foldername);
    fileMetadata.setParents(Collections.singletonList(parentFolderId));
    fileMetadata.setMimeType("application/vnd.google-apps.folder");

    File file = service.files().create(fileMetadata)
              .setFields("id")
              .execute();
  	return file.getId();
  }
}
