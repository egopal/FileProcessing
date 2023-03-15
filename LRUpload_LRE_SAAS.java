package Runners;

import java.io.File;
import java.io.IOException;
import java.math.BigInteger;
import java.net.ProxySelector;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.Arrays;
import java.util.Base64;
import java.util.List;
import java.util.Random;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import RunnersCore.MultipartUtility;

public class LRUpload_LRE_SAAS {
	
	public X509Certificate[] getAcceptedIssuers() {return null;}
    public void checkClientTrusted(X509Certificate[] certs, String authType) {}
    public void checkServerTrusted(X509Certificate[] certs, String authType) {}
    public boolean verify(String hostname, SSLSession session) {return true;}

	public static void main(String[] args) throws Throwable {
		
		String sessionCookie = lrAuthenticate();
		
		System.out.println("SessionCookie : "+ sessionCookie);
		
		if (sessionCookie != "") {
			String LREDomainScriptsPath = "Subject\\MMH\\MPO\\Services\\Scripts";
			String zipDirFilePath       = "C:\\EPE\\AIP_MAPD_Claim_ClaimsDetails.zip";
			lrUploadScript(sessionCookie, LREDomainScriptsPath, zipDirFilePath);
		}
		else {
			System.out.println("Please check LR Authentication");
		}
	}

	private static void lrUploadScript(String sessionCookie, String LREDomainScriptsPath, String zipDirFilePath) {

		String charset     = "UTF-8";
		String requestURL  = "https://lreorgprod4-pst.saas.microfocus.com/Loadtest/rest/domains/Cloud/projects/SDMC/Scripts";
		String boundary    = new BigInteger(128, new Random()).toString();
		String lreDirPath  = LREDomainScriptsPath;
		File   zipFilePath = new File(zipDirFilePath);
		String metaData    = "<Script xmlns=\"http://www.hp.com/PC/REST/API\">"
								+ "<TestFolderPath>"+lreDirPath+"</TestFolderPath>"
								+ "<Overwrite>true</Overwrite>"
								+ "<RuntimeOnly>false</RuntimeOnly>"
								+ "<KeepCheckedOut>false</KeepCheckedOut>"
								+ "</Script>";
		System.out.println("Request Data : " +metaData);

		try {
				MultipartUtility multipart;

				multipart = new MultipartUtility(requestURL, charset, sessionCookie);
				multipart.addFormField("metadata", metaData);
				multipart.addFilePart ("filename", zipFilePath);
				multipart.addHeaderField ("filename", metaData);
				
//				System.out.println("My Object : "+multipart.uploadRequest());
//				System.out.println("test : ");
				
				List<String> response = multipart.uploadRequest();
				System.out.println("SERVER REPLIED : ");
	
				for (String line : response) {
					System.out.println(line);
				}
				
		} catch (IOException ex) {
				// System.err.println(ex);
				ex.printStackTrace();
		}
	}
	
	private static String lrAuthenticate() throws IOException, InterruptedException {

		String encodedAuth = Base64.getEncoder()
				.encodeToString(("Jenkinsuser" + ":" + "Blue2023").getBytes(StandardCharsets.UTF_8));

		HttpRequest request = HttpRequest.newBuilder()
				.uri(URI.create("https://lreorgprod4-pst.saas.microfocus.com/Loadtest/rest/authentication-point/authenticate?tenant=88aa399d-b069-4115-8058-82621b2e1755"))
				.header("Authorization", "Basic " + encodedAuth).GET().build();

		System.out.println("Login Request : " + request);
		
		HttpResponse<String> loginResponse = HttpClient.newBuilder().proxy(ProxySelector.getDefault()).build()
				.send(request, HttpResponse.BodyHandlers.ofString());

		System.out.println("Login StatusCode : " + loginResponse.statusCode());
		System.out.println("headers : " + loginResponse.headers());

		String headerResponse = loginResponse.headers().map().toString();
		System.out.println("Login headers should have Cookie_Key:          " + headerResponse);

		String bodyResponse = loginResponse.body().lines().toString();
		System.out.println("Login body : ** " + bodyResponse);

		String cookie_Key = splitStringNew(headerResponse, "LWSSO_COOKIE_KEY=", ";");
		
		String cookie = "LWSSO_COOKIE_KEY="+cookie_Key;
		System.out.println("Login cookie : ** " + cookie_Key);
		
		return cookie;
	}
	
	public static String splitStringNew(String input, String start, String end) {
		
			System.out.println("SplitString - SessionCookie: " + input);

	     // String[] strArray = input.split("-|\\.");  
	        
			String firstcut, result = "";
			int startIndex = 0;
			int endIndex = input.length() - 1;
			System.out.println("int length: " + (endIndex+1));
			
			String[] strArray = input.split(start);  
		//	System.out.println("firstcut :"+Arrays.toString(strArray));
			firstcut = strArray[1].toString();
			System.out.println("firstcut :"+firstcut);
			
			String[] strArrEnd = firstcut.split(end);  
		//	System.out.println("Secondcut :"+Arrays.toString(strArrEnd));
			result = strArrEnd[0].toString();
			System.out.println("Secondcut :"+Arrays.toString(strArrEnd));
				
	        return result;
		}
		
	
	public static String splitString(String input, String start, String end) {

		String result = "";
		int startIndex = 0;
		int endIndex = input.length() - 1;

		if (start != null)
			startIndex = input.indexOf(start) + start.length();
		if (end != null)
			endIndex = input.indexOf(end);

		if (endIndex >= startIndex)
			result = input.substring(startIndex, endIndex);

		return result;
	}
}