import { Injectable } from '@angular/core';
import { DateTime } from 'luxon';
import { SseClient } from 'ngx-sse-client';
import { Subject, map, takeUntil } from 'rxjs';
import { Document } from '../../modules/copilot/copilot/copilot.component';

export type Inquire = {
  question: string;
  options: Array<string>;
  allows_input: boolean;
  input_label: string;
  input_placeholder: string;

  choices: Array<string>;
  input_value: string;
}

export type OutlineSubsection = {
  title: string;
}

export type OutlineSection = {
  title: string;
  subsections: Array<OutlineSubsection>;
}

export type Outline = {
  sections: Array<OutlineSection>;
}

export type NewDocument = {
  name: string;
  content: string;
}


export type WebSearchQuery = {
  query: string;
}


export type WebSearch = {
  queries: Array<WebSearchQuery>;
}

export type WebSearchResult = {
  query: string;
  title: string;
  url: string;
  text: string;
}

export type WebSearchResults = {
  results: Array<WebSearchResult>;
}

export type Message = {
  id: string
  date: string;
  hidden: boolean
  action?: 'inquire' | 'create-outline' | 'create-document' | 'search-web' | 'web-search-results';
  content?: string | null;

  inquire?: Inquire | null;
  outline?: Outline | null;
  document?: NewDocument | null;
  web_search_query?: WebSearch | null;
  web_search_results?: WebSearchResults | null;

  role: 'Assistant' | 'User' | 'Tool';
  status: 'Pending' | 'InProgress' | 'Completed' | 'Failed';
  created_at: string;
  updated_at: string;
}


export enum SSEEvent {
  Complete = 'Complete',
  Failed = 'Failed',
  Message = 'Message',
  Document = 'Document'
}

export interface SSEEventPayload {
  name: SSEEvent;
  body: any;
}

export interface SSEMessage {
  message?: Message | undefined;
  document?: Document | undefined;
  complete?: boolean | undefined;
}

@Injectable({
  providedIn: 'root'
})
export class MessageService {

  constructor(private sseClient: SseClient) { }

  public stream(messages: Array<Message>, document: Document, model: 'claude-3-haiku-20240307' | 'claude-3-sonnet-20240229' | 'claude-3-opus-20240229') {
    const url = `http://localhost:8080/stream`;

    const body = { messages, document, model };
    const streamComplete: Subject<void> = new Subject<void>();
    const stream$: Subject<SSEMessage> = new Subject<SSEMessage>();

    this.sseClient.stream(url, { keepAlive: false, reconnectionDelay: 5_000, responseType: 'event' }, { body }, 'POST').pipe(
      takeUntil(streamComplete)
    ).subscribe((event: any) => {
      console.log(event);

      if (event.type === 'error') {
        const errorEvent = event as ErrorEvent;
        console.error(errorEvent.error, errorEvent.message);

      } else {
        const messageEvent = event as MessageEvent;
        const payload: SSEEventPayload = JSON.parse(messageEvent.data);
        const sseMessage: SSEMessage = {};

        if (payload.name === SSEEvent.Message) {
          sseMessage.message = payload.body;
          stream$.next(sseMessage); // Emit the SSEMessage object

        } else if (payload.name === SSEEvent.Document) {
          sseMessage.document = payload.body;
          stream$.next(sseMessage); // Emit the SSEMessage object

        } else if (payload.name === SSEEvent.Complete) {
          sseMessage.complete = true;
          console.log("Calling Stream Complete");
          streamComplete.complete();

        } else {
          streamComplete.next();
          // throw new Error(payload.body); // Throw an error with the payload body
        }
      }
    });

    return stream$.asObservable();
  };

  public getCurrentUtcTimestamp(): string {
    return DateTime.local().toUTC().toISO(); // Get current UTC time in ISO format with timezone
  }
}
