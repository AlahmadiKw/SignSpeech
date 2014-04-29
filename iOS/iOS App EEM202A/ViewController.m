//
//  ViewController.m
//  BLEChat
//
//  Created by Cheong on 15/8/12.
//  Copyright (c) 2012 RedBear Lab., All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    
    bleShield = [[BLE alloc] init];
    [bleShield controlSetup];
    bleShield.delegate = self;
    [[self.textViewData layer] setBorderColor:[[UIColor grayColor] CGColor]];
    [[self.textViewData layer] setBorderWidth:2.3];
    [[self.textViewData layer] setCornerRadius:15];
    self.ipAddress.delegate = self;
    
    //Instantiate the object that will allow us to use text to speech
    self.speechSynthesizer = [[AVSpeechSynthesizer alloc] init];
    [self.speechSynthesizer setDelegate:self];
   // [self initNetworkCommunication];
    self.navigationItem.leftBarButtonItem = nil;
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

// --------ADDED--------------
- (BOOL)textFieldShouldReturn:(UITextField *)textField{
    NSLog(@"Text Field contents %@",textField.text);
    [textField resignFirstResponder];
    return YES;
}
- (IBAction) clickedBackground{
    
}
- (void)initNetworkCommunication {
    CFReadStreamRef readStream;
    CFWriteStreamRef writeStream;
    
    
    NSString *ip  = [NSString stringWithFormat: @"%@", self.ipAddress.text];
    CFStreamCreatePairWithSocketToHost(NULL, (__bridge CFStringRef)(ip), 80, &readStream, &writeStream);

    inputStream = (__bridge_transfer NSInputStream *)readStream;
    outputStream = (__bridge_transfer NSOutputStream *)writeStream;
    [inputStream setDelegate:self];
    [outputStream setDelegate:self];
    [inputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
    [outputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
    [inputStream open];
    [outputStream open];
}

- (IBAction)joinHost:(UIBarButtonItem *)sender {
    [self initNetworkCommunication];
}



- (void) sendToServer:(NSString *)message {
    NSString *response  = [NSString stringWithFormat:@"%@", message];
	NSData *data = [[NSData alloc] initWithData:[response dataUsingEncoding:NSASCIIStringEncoding]];
	[outputStream write:[data bytes] maxLength:[data length]];
}

- (void)stream:(NSStream *)theStream handleEvent:(NSStreamEvent)streamEvent {
    
	switch (streamEvent) {
        
        case NSStreamEventNone:
            self.HostButton.title = @"Connect Server";
            self.HostButton.tintColor = [UIColor redColor];
            
            
		case NSStreamEventOpenCompleted:
            self.HostButton.title = @"Disconnect Server";
            self.HostButton.tintColor = [UIColor greenColor];
			NSLog(@"Stream opened");
			break;
            
		case NSStreamEventHasBytesAvailable:
            if (theStream == inputStream) {
                
                uint8_t buffer[1024];
                int len;
                
                while ([inputStream hasBytesAvailable]) {
                    len = [inputStream read:buffer maxLength:sizeof(buffer)];
                    if (len > 0) {
                        
                        NSString *output = [[NSString alloc] initWithBytes:buffer length:len encoding:NSASCIIStringEncoding];
                        
                        if (nil != output) {
                            NSLog(@"server said: %@", output);
                            NSString *str1 = self.textViewData.text;
                            self.textViewData.text = [str1  stringByAppendingString: output];
                        }
                    }
                }
            }
			break;
            
		case NSStreamEventErrorOccurred:
			NSLog(@"Can not connect to the host!");
			break;
            
		case NSStreamEventEndEncountered:
			break;
            
		default:
			NSLog(@"Unknown event");
	}
    
}
// ---------------------------


// Called when scan period is over to connect to the first found peripheral
-(void) connectionTimer:(NSTimer *)timer
{
    if(bleShield.peripherals.count > 0)
    {
        [bleShield connectPeripheral:[bleShield.peripherals objectAtIndex:0]];
    }
    else
    {
        [self.spinner stopAnimating];
    }
}

-(void) bleDidReceiveData:(unsigned char *)data length:(int)length
{
    NSData *d = [NSData dataWithBytes:data length:length];
    NSString *s = [[NSString alloc] initWithData:d encoding:NSUTF8StringEncoding];
//    self.label.text = s;
//    NSString *str1 = self.textViewData.text;
//    self.textViewData.text = [str1  stringByAppendingString:s];
    NSLog(@"%@",s);
    [ self sendToServer:s];
    //self.textViewData.text = s;
}

NSTimer *rssiTimer;

-(void) readRSSITimer:(NSTimer *)timer
{
    [bleShield readRSSI];
}

- (void) bleDidDisconnect
{

    
//    [self.buttonBarConnect setTitle:@"Connect" forState: UIControlStateNormal];
    self.connectToArduino.title = @"Connect Device";
    self.connectToArduino.tintColor = [UIColor redColor];
    
    
    [rssiTimer invalidate];
}

-(void) bleDidConnect
{
    [self.spinner stopAnimating];

    
//    [self.buttonBarConnect setTitle:@"Disconnect" forState: UIControlStateNormal];
    self.connectToArduino.title = @"Disconnect Device";
    self.connectToArduino.tintColor = [UIColor greenColor];
    
    // Schedule to read RSSI every 1 sec.
    rssiTimer = [NSTimer scheduledTimerWithTimeInterval:(float)1.0 target:self selector:@selector(readRSSITimer:) userInfo:nil repeats:YES];
}


- (IBAction)clearText:(id)sender {
    self.textViewData.text = @"";
}


- (void)speakText:(NSString *)toBeSpoken{
    
    AVSpeechUtterance *utt = [AVSpeechUtterance speechUtteranceWithString:toBeSpoken];
    utt.rate = [self.speedSlider value];
    [self.speechSynthesizer speakUtterance:utt];
    
}
- (IBAction)speakButtonWasPressed:(id)sender {
 [self speakText:self.textViewData.text];
}

- (IBAction)speechSpeedShouldChange:(id)sender {
    UISlider *slider = (UISlider *)sender;
    NSInteger val = lround(slider.value);
    NSLog(@"%@",[NSString stringWithFormat:@"%ld",(long)val]);
}



-(void) bleDidUpdateRSSI:(NSNumber *)rssi
{
    self.labelRSSI.text = rssi.stringValue;
}

- (IBAction)BLEShieldSend:(id)sender
{
    NSString *s;
    NSData *d;
    
    if (self.textField.text.length > 16)
        s = [self.textField.text substringToIndex:16];
    else
        s = self.textField.text;

    s = [NSString stringWithFormat:@"%@\r\n", s];
    d = [s dataUsingEncoding:NSUTF8StringEncoding];
    
    [bleShield write:d];
}

- (IBAction)BLEShieldScan:(id)sender
{
    if (bleShield.activePeripheral)
        if(bleShield.activePeripheral.isConnected)
        {
            [[bleShield CM] cancelPeripheralConnection:[bleShield activePeripheral]];
            return;
        }
    
    if (bleShield.peripherals)
        bleShield.peripherals = nil;
    
    [bleShield findBLEPeripherals:3];
    
    [NSTimer scheduledTimerWithTimeInterval:(float)3.0 target:self selector:@selector(connectionTimer:) userInfo:nil repeats:NO];
    
    [self.spinner startAnimating];
}

@end
