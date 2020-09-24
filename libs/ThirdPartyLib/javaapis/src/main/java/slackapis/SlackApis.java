package slackapis;
import com.slack.api.methods.MethodsClient;
import com.slack.api.methods.request.chat.ChatPostMessageRequest;
import com.slack.api.methods.response.chat.ChatPostMessageResponse;
import com.slack.api.Slack;
import com.slack.api.model.Message;
import com.slack.api.methods.request.files.FilesUploadRequest;
import java.io.File;
import com.slack.api.methods.response.files.FilesUploadResponse;
import java.util.ArrayList;
import java.util.List;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import com.slack.api.methods.SlackApiException;
import java.io.IOException;

public class SlackApis {
	
	private String token;
	private String channel;
	
	public SlackApis(String token, String channel){
		this.token = token;
		this.channel = channel;
  	}

    public void sendMessage(String mentionUser, String appName, String text) {
    	
    Slack slack = Slack.getInstance();
    String token = this.token;

    // API メソッドのクライアントを上のトークンと共に初期化します
    MethodsClient methods = slack.methods(token);

    // API リクエスト内容を構成します
    ChatPostMessageRequest request = ChatPostMessageRequest.builder()
    .channel(this.channel) // ここでは簡単に試すためにチャンネル名を指定していますが `C1234567` のような ID を指定する方が望ましいです
    .text("<@" + mentionUser +">["+ appName + "]" + text)
    .build();

    
    try {
        // API レスポンスを Java オブジェクトとして受け取ります
        ChatPostMessageResponse response = methods.chatPostMessage(request);
        if (response.isOk()) {
            Message postedMessage = response.getMessage();
        } else {
            String errorCode = response.getError(); // 例: "invalid_auth", "channel_not_found"
            System.out.println(errorCode);
        }
    } catch (Exception e) {
        System.out.println("Failed to send.");
    }

    }
	
	public void uploadImage(String mentionUser, String appName, String text, String fileName) throws IOException, SlackApiException {
		Slack slack = Slack.getInstance();
    	String token = this.token;

    	// API メソッドのクライアントを上のトークンと共に初期化します
    	MethodsClient methods = slack.methods(token);


    	List<String> channels = new ArrayList<String>();
    	channels.add(this.channel);
		Path file = Paths.get(fileName);
    	byte[] bytes = Files.readAllBytes(file);
    	
    	// API リクエスト内容を構成します
    	FilesUploadRequest request = FilesUploadRequest.builder()
    	.channels(channels)
    	.initialComment("<@" + mentionUser +">["+ appName + "]" + text)
		.fileData(bytes)
    	.filename(file.getFileName().toString())
    	.filetype("png")
    	.build();
		
    	// API レスポンスを Java オブジェクトとして受け取ります
    	FilesUploadResponse response = methods.filesUpload(request);
    	if (response.isOk()) {
    	} else {
    	    String errorCode = response.getError(); // 例: "invalid_auth", "channel_not_found"
    	    System.out.println(errorCode);
    	}

    }

}