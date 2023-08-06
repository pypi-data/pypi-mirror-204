import type { IGWProps } from '@kanaries/graphic-walker/dist/App';
export interface IAppProps extends IGWProps {
    version?: string;
    hashcode?: string;
    visSpec?: string;
    userConfig?: {
        [key: string]: any;
    };
}
