import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, ChangeDetectorRef, Component, ElementRef, ViewChild } from '@angular/core';
import { Subject } from 'rxjs';
import { Message, MessageService, SSEMessage } from '../../../services/message/message.service';
import { FormControl, FormGroup, FormsModule } from '@angular/forms';
import { PromptEditorComponent } from '../components/prompt-editor/prompt-editor.component';
import { PromptSuggestionsComponent } from '../components/prompt-suggestions/prompt-suggestions.component';
import { DocumentComponent } from '../../document/document/document.component';
import { MessageComponent } from '../components/message/message.component';
import { v4 as uuidv4 } from 'uuid';
import { InquireActionComponent } from '../components/actions/inquire-action/inquire-action.component';
import { OutlineActionComponent } from '../components/actions/outline-action/outline-action.component';
import { WebSearchActionComponent } from '../components/actions/web-search-action/web-search-action.component';
import { WebSearchResultsComponent } from '../components/actions/web-search-results/web-search-results.component';

export type Document = {
  id: string
  name: string;
  content: string;
  created_at: string;
  updated_at: string;
}


@Component({
  selector: 'app-copilot',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,

    PromptSuggestionsComponent,
    PromptEditorComponent,
    DocumentComponent,
    
    MessageComponent,
    InquireActionComponent,
    OutlineActionComponent,
    WebSearchActionComponent,
    WebSearchResultsComponent
  ],
  templateUrl: './copilot.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CopilotComponent {

  @ViewChild(PromptEditorComponent) public promptEditor: PromptEditorComponent | undefined;
  @ViewChild('scrollContainer') scrollContainer: ElementRef | undefined

  public destroyed$: Subject<void> = new Subject<void>();

  public processing: boolean = false;

  public model: 'claude-3-haiku-20240307' | 'claude-3-sonnet-20240229' | 'claude-3-opus-20240229' = 'claude-3-haiku-20240307';
  public messages: Message[] = [];

  public firstTokenArrived: boolean = false;

  public documentForm: FormGroup = new FormGroup({
    name: new FormControl(''),
    content: new FormControl('')
  })

  constructor(private cdr: ChangeDetectorRef, private messageService: MessageService) {

  }

  ngAfterViewInit(): void {
    this.focus();
  }

  public focus(): void {
    this.promptEditor?.focus();
  }

  public newSession(): void {
    this.messages = [];
    this.documentForm.reset();
  }

  trackByUpdatedAt(index: number, message: Message): string {
    return message.updated_at;
  }

  public stream(prompt: string, hidden: boolean = false): void {
    // Streams a completion from the assistant
    this.processing = true;
    this.firstTokenArrived = false;

    const message: Message = {
      id: uuidv4(),
      date: this.messageService.getCurrentUtcTimestamp(),
      hidden: hidden,
      role: 'User',
      status: 'Completed',
      content: prompt,
      created_at: this.messageService.getCurrentUtcTimestamp(),
      updated_at: this.messageService.getCurrentUtcTimestamp()
    }

    const document: Document = {
      id: uuidv4(),
      name: this.documentForm.get('name')?.value,
      content: this.documentForm.get('content')?.value,
      created_at: this.messageService.getCurrentUtcTimestamp(),
      updated_at: this.messageService.getCurrentUtcTimestamp()
    }

    this.messages.push(message);

    this.cdr.detectChanges();

    this.messageService.stream(this.messages, document, this.model).subscribe({
      next: (response: SSEMessage) => {
        console.log(response);
        this.firstTokenArrived = true;

        if (response.document) {
          // Fill the document form when the document is streamed
          this._fillDocumentForm(response.document.name, response.document.content);
          this.cdr.detectChanges();
        } else if (response.message) {
          // Update the messages array with the streamed message
          this._updateMessages(response.message);
        }
        this.cdr.detectChanges();
      },
      error: (error: any) => {
        console.log("Failed to stream messages", error);
        this.processing = false;
        this.documentForm.reset();
        this.messages = [];
        
        this.cdr.detectChanges();
      },

      complete: () => {
        console.log("Completed streaming messages");
        this.processing = false;
        this.focus();
        this.cdr.detectChanges();
      }
    })
  }

  private _updateMessages(message: Message): void {
    const messageIndex = this.messages.findIndex(m => m.id === message?.id);
    if (messageIndex !== -1) {
      this.messages[messageIndex] = message;
    } else {
      this.messages.push(message!);
    }
  }

  private _fillDocumentForm(name: string, content: string): void {
    this.documentForm.get('name')?.setValue(name);
    this.documentForm.get('content')?.setValue(content);
  }

}
