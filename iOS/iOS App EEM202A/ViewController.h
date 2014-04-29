//
//  ViewController.h
//  BLEChat
//
//  Created by Cheong on 15/8/12.
//  Copyright (c) 2012 RedBear Lab., All rights reserved.
//

#import <AVFoundation/AVFoundation.h>
#import <UIKit/UIKit.h>
#import <AudioToolbox/AudioToolbox.h>
#import <QuartzCore/QuartzCore.h> 
#import "BLE.h"


@interface ViewController : UIViewController <BLEDelegate, UITextViewDelegate, NSStreamDelegate, UITextFieldDelegate> {
    BLE *bleShield;
    NSInputStream *inputStream;
    NSOutputStream *outputStream;
}


@property (weak, nonatomic) IBOutlet UIActivityIndicatorView *spinner;
@property (weak, nonatomic) IBOutlet UITextField *textField;
//@property (weak, nonatomic) IBOutlet UILabel *label;
@property (weak, nonatomic) IBOutlet UILabel *labelRSSI;
//@property (weak, nonatomic) IBOutlet UIButton *buttonConnect;
@property (weak, nonatomic) IBOutlet UIButton *buttonBarConnect;
@property (weak, nonatomic) IBOutlet UIBarButtonItem *connectToArduino;
@property (weak, nonatomic) IBOutlet UITextView *textViewData;
@property (weak, nonatomic) IBOutlet UIBarButtonItem *HostButton;


@property (nonatomic, retain) AVSpeechSynthesizer *speechSynthesizer;
@property (weak, nonatomic) IBOutlet UISlider *speedSlider;
@property (weak, nonatomic) IBOutlet UITextField *ipAddress;

// ------ADDED-----
- (BOOL)textFieldShouldReturn:(UITextField *)textField;
- (IBAction) clickedBackground;
// ------TCP-------
- (IBAction)joinHost:(id)sender;

// ----------------

@end
